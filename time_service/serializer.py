from .models import TimeIn,TimeOut
from rest_framework import serializers

class TimeInSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeIn
        fields = '__all__'

class TimeOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeOut
        fields = '__all__'