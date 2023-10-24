from django.shortcuts import render
from .models import Setting
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import SettingSerializer
from rest_framework import status
from user_service.jsonwebtokens import verify_jwt
from user_service.models import User,Account
from user_service.serializer import UserSerializer

# Create your views here.

def checkAuthorization(request):
    authorization_header = request.META.get('HTTP_AUTHORIZATION')
    decoded_data=verify_jwt(authorization_header)
    if isinstance(decoded_data, dict)==False:
        return 1
    else:
        authorization=User.objects.get(id_user=decoded_data['data']['id_user'])
        account_authorization=Account.objects.get(user=authorization)
        if authorization is not None and account_authorization is not None:
            return 0
    return 2

@api_view(['PUT'])
def update_setting(request):
    checkAu=checkAuthorization(request)
    if checkAu==0:
        setting=Setting.objects.get(id_setting=1)
        data=request.GET
        if setting is not None:
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
        serializer = SettingSerializer(Setting())
        return Response({"data":serializer.data,"message":"Not found","code":404},status=status.HTTP_200_OK)
    elif checkAu==1:
        serializer = UserSerializer(Setting())
        return Response({"data":serializer.data,"message":"Expired","code":401},status=status.HTTP_200_OK)
    else:
        serializer = UserSerializer(Setting())
        return Response({"data":serializer.data,"message":"Failed","code":400},status=status.HTTP_200_OK)
    
@api_view(['GET'])
def get_setting(request):
    checkAu=checkAuthorization(request)
    if checkAu==0:
        setting=Setting.objects.get(id_setting=1)
        if setting is not None:
            serializer = SettingSerializer(setting)
            return Response({"data":serializer.data,"message":"Success","code":200},status=status.HTTP_200_OK)
        serializer = SettingSerializer(Setting())
        return Response({"data":serializer.data,"message":"Not found","code":404},status=status.HTTP_200_OK)
    elif checkAu==1:
        serializer = UserSerializer(Setting())
        return Response({"data":serializer.data,"message":"Expired","code":401},status=status.HTTP_200_OK)
    else:
        serializer = UserSerializer(Setting())
        return Response({"data":serializer.data,"message":"Failed","code":400},status=status.HTTP_200_OK)

    