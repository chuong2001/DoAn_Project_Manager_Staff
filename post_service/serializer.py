from .models import Image,Post
from rest_framework import serializers
from user_service.serializer import UserSerializer

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    images=ImageSerializer()
    class Meta:
        model = Post
        fields = '__all__'
        

        