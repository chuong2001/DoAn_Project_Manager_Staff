from .models import Calendar,TypeCalendar
from rest_framework import serializers

class TypeTypeCalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeCalendar
        fields = '__all__'

class CalendarSerializer(serializers.ModelSerializer):
    type_calendar = TypeTypeCalendarSerializer()
    class Meta:
        model = Calendar
        fields = '__all__'

    
        