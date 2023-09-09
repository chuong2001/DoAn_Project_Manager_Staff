from .models import TimeIn,TimeOut
from rest_framework import serializers

class TimeInSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeIn
        fields = ("id","day_in","time_in")

class TimeOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeOut
        fields = ("id","day_out","time_out")