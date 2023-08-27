from django.shortcuts import render
from .models import TimeIn,TimeOut
from user_service.models import User
from rest_framework.decorators import api_view
from user_service.serializer import UserSerializer
from rest_framework.response import Response
from .serializer import TimeInSerializer,TimeOutSerializer
from rest_framework import status
from django.db.models import Q

# Create your views here.

@api_view(['POST'])
def add_time(request,id_user):
    data=request.GET
    user=User.objects.get(id_user=id_user)
    if user:
        list_time_ins= TimeIn.objects.filter(user=user)
        list_time_outs=TimeOut.objects.filter(user=user)
        day=data.get("day")
        time=data.get("time")
        
        if len(list_time_ins)==len(list_time_outs):
            TimeIn.objects.create(day_in=day,time_in=time,user=user)
        else:
            TimeOut.objects.create(day_out=day,time_out=time,user=user)
        serializer = UserSerializer(user)
        return Response({"data":serializer.data,"message":"Success","code":200},status=status.HTTP_200_OK)
    return Response({"data":"","message":"Failded","code":400},status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_time_user(request,id_user):
    data=request.GET
    day_start=data.get("day_start")
    day_end=data.get("day_end")
    user=User.objects.get(id_user=id_user)
    if user:
        serializer = UserSerializer(user, context={'start_day': day_start, 'end_day': day_end})
        return Response({"data":serializer.data,"message":"Success","code":200},status=status.HTTP_200_OK)
    return Response({"data":"","message":"Failded","code":400},status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_time_all(request):
    data=request.GET
    day_start=data.get("day_start")
    day_end=data.get("day_end")
    list_user=User.objects.all()
    serializer = UserSerializer(list_user,Many=True, context={'start_day': day_start, 'end_day': day_end})
    return Response({"data":serializer.data,"message":"Success","code":200},status=status.HTTP_200_OK)