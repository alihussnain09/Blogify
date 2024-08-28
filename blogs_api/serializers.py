from rest_framework import serializers
from blogs.models import blog_post, Category, Tag, Comment
from django.contrib.auth.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username','password','email']
        
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )
        return user
        

class BlogPostSerializer(serializers.ModelSerializer):
    
    author = serializers.StringRelatedField()
    # tags = serializers.StringRelatedField(many = True)
    likes = serializers.StringRelatedField(many = True)
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='name'
    )
    tags = serializers.SlugRelatedField(
        queryset=Tag.objects.all(),
        slug_field='name',
        many=True
    )
    
    
    class Meta:
        model = blog_post
        fields = '__all__'
        
class CommentSerializer(serializers.ModelSerializer):
    Author = serializers.ReadOnlyField(source='Author.username') 

    class Meta:
        model = Comment
        fields = ['id', 'blog', 'Author', 'content', 'date_posted']
        read_only_fields = ['Author', 'date_posted']
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
