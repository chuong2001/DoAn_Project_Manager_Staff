from .models import TimeIn,TimeOut
from user_service.serializer import UserSerializer
from rest_framework import serializers

class TimeInSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeIn
        fields = ("day_in","time_in")

class TimeOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeOut
        fields = ("day_out","time_out")