from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import CalendarSerializer
from .models import Calendar
from rest_framework import status
from user_service.models import Part
from datetime import datetime

# Create your views here.
@api_view(['GET'])
def list_calender_by_part(request,id_part):
    part=Part.objects.get(id_part=id_part)
    print(part.name_part)
    data=request.GET
    if part:
        day=data.get('day_calendar')
        list_calendar=Calendar.objects.filter(part=part,day_calendar=day)
        list_calendar_formats=[]
        for calendar in list_calendar:
            date_object = datetime.strptime(str(calendar.day_calendar), "%Y-%m-%d")
            new_date_string = date_object.strftime("%d-%m-%Y")  
            calendar.set_day_calendar(new_date_string)
            list_calendar_formats.append(calendar)
        serializer = CalendarSerializer(list_calendar_formats,many=True)
        return Response({"data":serializer.data,"message":"Success","code":200},status=status.HTTP_200_OK)
    serializer = CalendarSerializer([],many=True)
    return Response({"data":serializer.data,"message":"Failded","code":400},status=status.HTTP_400_BAD_REQUEST)