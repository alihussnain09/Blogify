from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

class Category(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='tags')
    
    def __str__(self):
        return self.name

class blog_post(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/',blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null= True)
    tags = models.ManyToManyField(Tag ,blank=True)
    likes = models.ManyToManyField(User,related_name='liked_posts',blank=True)
    
    def total_likes(self):
        return self.likes.count()
    def __str__(self):
        return self.title

class Comment(models.Model):
    blog = models.ForeignKey(blog_post, related_name='comments',on_delete=models.CASCADE)
    Author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Comment by {self.author} on {self.blog}'
