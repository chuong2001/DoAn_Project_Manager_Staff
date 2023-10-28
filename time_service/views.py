from django.shortcuts import render
from .models import TimeIn,TimeOut
from user_service.models import User,Account
from rest_framework.decorators import api_view
from user_service.serializer import UserSerializer
from rest_framework.response import Response
from .serializer import TimeInSerializer,TimeOutSerializer
from rest_framework import status
from datetime import datetime
from notification_service.models import NotificationPost
from django.db.models import Q
from user_service.jsonwebtokens import create_jwt,verify_jwt

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


@api_view(['POST'])
def add_time(request,id_user):
    checkAu=checkAuthorization(request)
    if checkAu==0:
        data=request.GET
        user=User.objects.get(id_user=id_user)
        if user is not None:
            list_time_ins= TimeIn.objects.filter(user=user)
            list_time_outs=TimeOut.objects.filter(user=user)
            day=data.get("day")
            time=data.get("time")
            
            date_obj = datetime.strptime(day, '%Y-%m-%d')
            new_s = date_obj.strftime('%d-%m-%Y')
            
            if len(list_time_ins)==len(list_time_outs):
                timein=TimeIn()
                timein.set_day_in(day)
                timein.set_time_in(time)
                timein.set_user(user)
                timein.save()
                NotificationPost.objects.create(title_notification='Chấm công thành công',body_notification='Bạn vừa đến công ty vào ngày '+new_s+' lúc '+time,time_notification=day+' '+time,is_read=0,type_notification=2,id_data=timein.id_time_in,user=user)
            else:
                timeout=TimeOut()
                timeout.set_day_out(day)
                timeout.set_time_out(time)
                timeout.set_user(user)
                timeout.save()
                NotificationPost.objects.create(title_notification='Chấm công thành công',body_notification='Bạn vừa rời công ty vào ngày '+new_s+' lúc '+time,time_notification=day+' '+time,is_read=0,type_notification=2,id_data=timeout.id_time_out,user=user)

            
            serializer = UserSerializer(user)
            return Response({"data":serializer.data,"message":"Success","code":201},status=status.HTTP_201_CREATED)
        serializer = UserSerializer(User())
        return Response({"data":serializer.data,"message":"Not found","code":404},status=status.HTTP_200_OK)
    elif checkAu==1:
        serializer = UserSerializer(User())
        return Response({"data":serializer.data,"message":"Expired","code":401},status=status.HTTP_200_OK)
    else:
        serializer = UserSerializer(User())
        return Response({"data":serializer.data,"message":"Failed","code":400},status=status.HTTP_200_OK)


@api_view(['GET'])
def get_time_user(request,id_user):
    checkAu=checkAuthorization(request)
    if checkAu==0:
        data=request.GET
        day_start=data.get("day_start")
        day_end=data.get("day_end")
        date_object1 = datetime.strptime(day_start, "%d-%m-%Y")
        start_day_new = date_object1.strftime("%Y-%m-%d")   
        date_object2 = datetime.strptime(day_end, "%d-%m-%Y")
        end_day_new = date_object2.strftime("%Y-%m-%d") 
        user=User.objects.get(id_user=id_user)
        if user is not None:
            serializer = UserSerializer(user, context={'start_day': start_day_new, 'end_day': end_day_new})
            return Response({"data":serializer.data,"message":"Success","code":200},status=status.HTTP_200_OK)
        serializer = UserSerializer(User())
        return Response({"data":serializer.data,"message":"Not found","code":404},status=status.HTTP_200_OK)
    elif checkAu==1:
        serializer = UserSerializer(User())
        return Response({"data":serializer.data,"message":"Expired","code":401},status=status.HTTP_200_OK)
    else:
        serializer = UserSerializer(User())
        return Response({"data":serializer.data,"message":"Failed","code":400},status=status.HTTP_200_OK)

@api_view(['GET'])
def get_time_all(request):
    checkAu=checkAuthorization(request)
    if checkAu==0:
        data=request.GET
        day_start=data.get("day_start")
        day_end=data.get("day_end")
        list_user=User.objects.all()
        serializer = UserSerializer(list_user,Many=True, context={'start_day': day_start, 'end_day': day_end})
        return Response({"data":serializer.data,"message":"Success","code":200},status=status.HTTP_200_OK)
    elif checkAu==1:
        serializer = UserSerializer(User())
        return Response({"data":serializer.data,"message":"Expired","code":401},status=status.HTTP_200_OK)
    else:
        serializer = UserSerializer(User())
        return Response({"data":serializer.data,"message":"Failed","code":400},status=status.HTTP_200_OK)