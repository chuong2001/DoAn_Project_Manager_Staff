from .models import Comment
from rest_framework import serializers
from user_service.serializer import UserSerializer
from post_service.serializer import PostSerializer

class CommentSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    post=PostSerializer()
    class Meta:
        model = Comment
        fields = '__all__'
    
        