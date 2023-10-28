from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import CalendarSerializer,TypeTypeCalendarSerializer
from .models import Calendar,TypeCalendar
from rest_framework import status
from user_service.models import Part,User,Account
from django.db.models import Q
from datetime import datetime
from user_service.jsonwebtokens import verify_jwt
from notification_service.models import NotificationPost

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

# Create your views here.
@api_view(['GET'])
def list_calender_by_part(request,id_part):
    checkAu=checkAuthorization(request)
    if checkAu==0:
        part=Part.objects.get(id_part=id_part)
        data=request.GET
        if part is not None:
            day=data.get('day_calendar')
            list_calendar=Calendar.objects.filter(part=part,day_calendar=day).order_by('time_start')
            list_calendar_formats=[]
            for calendar in list_calendar:
                date_object = datetime.strptime(str(calendar.day_calendar), "%Y-%m-%d")
                new_date_string = date_object.strftime("%d-%m-%Y")  
                calendar.set_day_calendar(new_date_string)
                list_calendar_formats.append(calendar)
            serializer = CalendarSerializer(list_calendar_formats,many=True)
            return Response({"data":serializer.data,"message":"Success","code":200},status=status.HTTP_200_OK)
        return Response({"data":[],"message":"Not found","code":404},status=status.HTTP_200_OK)
    elif checkAu==1:
        return Response({"data":[],"message":"Expired","code":401},status=status.HTTP_200_OK)
    else:
        return Response({"data":[],"message":"Failed","code":400},status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_calendar(request,id_calendar):
    checkAu=checkAuthorization(request)
    if checkAu==0:
        calendar=Calendar.objects.get(id_calendar=id_calendar)
        if calendar is not None:
            listNotification=NotificationPost.objects.filter(Q(type_notification=5) & Q(id_data=calendar.id_calendar))
            for notification in listNotification:
                notification.delete()
            calendar.delete()
            return Response({"data":"","message":"Success","code":200},status=status.HTTP_200_OK)
        return Response({"data":"","message":"Not found","code":404},status=status.HTTP_200_OK)
    elif checkAu==1:
        return Response({"data":"","message":"Expired","code":401},status=status.HTTP_200_OK)
    else:
        return Response({"data":"","message":"Failed","code":400},status=status.HTTP_200_OK)

@api_view(['GET'])
def all_type_calendar(request):
    checkAu=checkAuthorization(request)
    if checkAu==0:
        listTypeCalendar=TypeCalendar.objects.all()
        if listTypeCalendar is not None:
            serializer = TypeTypeCalendarSerializer(listTypeCalendar,many=True)
            return Response({"data":serializer.data,"message":"Success","code":200},status=status.HTTP_200_OK)
        return Response({"data":[],"message":"Not found","code":404},status=status.HTTP_200_OK)
    elif checkAu==1:
        return Response({"data":[],"message":"Expired","code":401},status=status.HTTP_200_OK)
    else:
        return Response({"data":[],"message":"Failed","code":400},status=status.HTTP_200_OK)

@api_view(['GET'])
def get_calendar(request,id_calendar):
    checkAu=checkAuthorization(request)
    if checkAu==0:
        calendar=Calendar.objects.get(id_calendar=id_calendar)
        if calendar is not None:
            serializer = CalendarSerializer(calendar)
            return Response({"data":serializer.data,"message":"Success","code":200},status=status.HTTP_200_OK)
        serializer = CalendarSerializer(Calendar())
        return Response({"data":serializer.data,"message":"Not found","code":404},status=status.HTTP_200_OK)
    elif checkAu==1:
        serializer = CalendarSerializer(Calendar())
        return Response({"data":serializer.data,"message":"Expired","code":401},status=status.HTTP_200_OK)
    else:
        serializer = CalendarSerializer(Calendar())
        return Response({"data":serializer.data,"message":"Failed","code":400},status=status.HTTP_200_OK)

def time_to_seconds(time_str):
    if len(time_str)>5:
        time_str=time_str[0:5]
    hours, minutes = map(int, time_str.split(':'))
    return hours * 3600 + minutes * 60

def is_overlapping(start1, end1, start2, end2):
    start1_seconds = time_to_seconds(start1)
    end1_seconds = time_to_seconds(end1)
    start2_seconds = time_to_seconds(start2)
    end2_seconds = time_to_seconds(end2)

    return (start1_seconds < end2_seconds and end1_seconds > start2_seconds)

@api_view(['POST'])
def add_calendar(request,id_part,id_type_calendar):
    checkAu=checkAuthorization(request)
    if checkAu==0:
        part=Part.objects.get(id_part=id_part)
        type_calendar=TypeCalendar.objects.get(id_type=id_type_calendar)
        data=request.GET
        if part is not None and type_calendar is not None:
            day_calendar=data.get('day_calendar')
            time_start=data.get('time_start')
            time_end=data.get('time_end')
            check=True
            listCalendar=Calendar.objects.filter(Q(part=part) & Q(day_calendar=day_calendar))
            if not listCalendar:
                check=True
            else:
                for calendar in listCalendar:
                    if is_overlapping(time_start,time_end,str(calendar.time_start),str(calendar.time_end)):
                        check=False
                        break
            if check:
                calendar = Calendar(part=part,
                header_calendar=data.get('header_calendar'),
                body_calendar=data.get('body_calendar'),
                address=data.get('address'),
                day_calendar=day_calendar,
                time_start=time_start,
                time_end=time_end,
                type_calendar=type_calendar)
                calendar.save()
                listUser=User.objects.filter(part=part)
                account=Account.objects.get(username='admin')
                for u in listUser:
                    NotificationPost.objects.create(title_notification=str(account.user.full_name)+' đã thêm lịch làm việc',body_notification=calendar.header_calendar,time_notification=calendar.day_calendar+' '+calendar.time_start,is_read=0,type_notification=5,id_data=calendar.id_calendar,user=u)
                return Response({"data":"","message":"Success","code":201},status=status.HTTP_201_CREATED)
            return Response({"data":"","message":"Exist","code":400},status=status.HTTP_200_OK)
        return Response({"data":"","message":"Not found","code":404},status=status.HTTP_200_OK)
    elif checkAu==1:
        return Response({"data":"","message":"Expired","code":401},status=status.HTTP_200_OK)
    else:
        return Response({"data":"","message":"Failed","code":400},status=status.HTTP_200_OK)

@api_view(['PUT'])
def update_calendar(request,id_calendar,id_part,id_type_calendar):
    checkAu=checkAuthorization(request)
    if checkAu==0:
        calendar=Calendar.objects.get(id_calendar=id_calendar)
        part=Part.objects.get(id_part=id_part)
        type_calendar=TypeCalendar.objects.get(id_type=id_type_calendar)
        data=request.GET
        if calendar is not None and type_calendar is not None and part is not None:
            day_calendar=data.get('day_calendar')
            time_start=data.get('time_start')
            time_end=data.get('time_end')
            check=True
            listCalendar=Calendar.objects.filter(Q(part=part) & Q(day_calendar=day_calendar))
            if not listCalendar:
                check=True
            else:
                for ca in listCalendar:
                    if ca.id_calendar!=id_calendar and is_overlapping(time_start,time_end,str(ca.time_start),str(ca.time_end)):
                        check=False
                        break
            if check:
                header_calendar=data.get('header_calendar')
                body_calendar=data.get('body_calendar')
                address=data.get('address')
                calendar.set_address(address)
                calendar.set_header_calendar(header_calendar)
                calendar.set_body_calendar(body_calendar)
                calendar.set_day_calendar(day_calendar)
                calendar.set_time_end(time_end)
                calendar.set_time_start(time_start)
                calendar.set_type_calendar(type_calendar)
                calendar.save()
                listNotification=NotificationPost.objects.filter(Q(type_notification=5) & Q(id_data=calendar.id_calendar))
                for notification in listNotification:
                    notification.set_body_notification(calendar.header_calendar)
                    notification.save()
                return Response({"data":"","message":"Success","code":200},status=status.HTTP_200_OK)
            return Response({"data":"","message":"Exist","code":400},status=status.HTTP_200_OK)
        return Response({"data":"","message":"Not found","code":404},status=status.HTTP_200_OK)
    elif checkAu==1:
        return Response({"data":"","message":"Expired","code":401},status=status.HTTP_200_OK)
    else:
        return Response({"data":"","message":"Failed","code":400},status=status.HTTP_200_OK)
