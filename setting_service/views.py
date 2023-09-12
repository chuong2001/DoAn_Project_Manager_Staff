from django.shortcuts import render
from .models import Setting
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import SettingSerializer
from rest_framework import status

# Create your views here.
@api_view(['PUT'])
def update_setting(request):
    setting=Setting.objects.get(id_setting=1)
    data=request.GET
    if setting:
        if data.get("time_start"):
            setting.set_time_start(data.get("time_start"))
            
        if data.get("time_end"):
            setting.set_time_end(data.get("time_end"))
            
        if data.get("overtime"):
            setting.set_overtime(data.get("overtime"))
            
        if data.get("holiday"):
            setting.set_holiday(data.get("holiday"))
            
        if data.get("day_off"):
            setting.set_day_off(data.get("day_off"))
         
        setting.save()   
        serializer = SettingSerializer(setting)
        return Response({"data":serializer.data,"message":"Success","code":200},status=status.HTTP_200_OK)
    return Response({"data":"","message":"Failded","code":400},status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def get_setting(request):
    setting=Setting.objects.get(id_setting=1)
    if setting:
        serializer = SettingSerializer(setting)
        return Response({"data":serializer.data,"message":"Success","code":200},status=status.HTTP_200_OK)
    return Response({"data":"","message":"Failded","code":400},status=status.HTTP_400_BAD_REQUEST)
    