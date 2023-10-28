from .models import NotificationPost
from rest_framework import serializers
from datetime import datetime

class NotificationPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationPost
        fields = '__all__'
