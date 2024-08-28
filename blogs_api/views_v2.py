from rest_framework import viewsets
from blogs.models import blog_post
from .serializers import BlogPostSerializer
from rest_framework.permissions import IsAuthenticated


class BlogPostViewSetV2(viewsets.ModelViewSet):
    queryset = blog_post.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)