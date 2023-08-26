from .models import TimeIn,TimeOut
from user_service.serializer import UserSerializer
from rest_framework import serializers

class TimeInSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model = TimeIn
        fields = '__all__'

class TimeOutSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model = TimeOut
        fields = '__all__'