from .models import Image,Post
from comment_service.models import Comment
from rest_framework import serializers
from comment_service.serializer import CommentSerializer
from user_service.serializer import UserSerializer

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ("id_image","image")

class PostSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()  
    comments = serializers.SerializerMethodField()  
    class Meta:
        model = Post
        fields = '__all__'

    def get_images(self, obj):
        images = Image.objects.filter(post=obj)
        return ImageSerializer(images, many=True).data
    
    def get_comments(self, obj):
        comments = Comment.objects.filter(post=obj)
        return CommentSerializer(comments, many=True).data
     