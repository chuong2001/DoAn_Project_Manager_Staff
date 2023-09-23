from .models import Calendar
from rest_framework import serializers

class CalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendar
        fields = '__all__'

    
        