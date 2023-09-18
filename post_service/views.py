from django.shortcuts import render
from .models import Post,Image
from comment_service.models import Comment
from user_service.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import PostSerializer
from rest_framework import status
from datetime import datetime
import pytz

# Create your views here.
@api_view(['POST'])
def add_post(request,id_user):
    data=request.GET
    user=User.objects.get(id_user=id_user)
    if user:
        post=Post(
        type_post=data.get("type_post"),
        header_post=data.get("header_post"),
        time_post=data.get("time_post"),
        content=data.get("content"),
        num_like=data.get("num_like"),
        num_comment=data.get("num_comment"),
        user=user)
        post.save()
        list_link_image=data.get("image").split()
        for link_image in list_link_image:
            Image.objects.create(image=link_image,post=post)
        serializer = PostSerializer(post)
        return Response({"data":serializer.data,"message":"Success","code":200},status=status.HTTP_200_OK)
    return Response({"data":"","message":"Failded","code":400},status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['PUT'])
def update_post(request,id_post):
    data=request.GET
    post=Post.objects.get(id_post=id_post)
    if post:
        post=Post(
        type_post=data.get("type_post"),
        header_post=data.get("header_post"),
        time_post=data.get("time_post"),
        content=data.get("content"),
        num_like=data.get("num_like"),
        num_comment=data.get("num_comment"))
        post.save()
        images_to_delete = Image.objects.filter(post=post)
        images_to_delete.delete()
        list_link_image=data.get("image").split()
        for link_image in list_link_image:
            Image.objects.create(image=link_image,post=post)
        serializer = PostSerializer(post)
        return Response({"data":serializer.data,"message":"Success","code":200},status=status.HTTP_200_OK)
    return Response({"data":"","message":"Failded","code":400},status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def all_post(request):
    list_post=Post.objects.all()
    list_post_new=[]
    if list_post:
        for post in list_post:
            specific_time = datetime.fromisoformat(str(post.time_post))
            time_string_without_offset = specific_time.strftime("%Y-%m-%d %H:%M:%S")
            input_time = datetime.strptime(time_string_without_offset, "%Y-%m-%d %H:%M:%S")
            time_formated_day = input_time.strftime("%d-%m-%Y")
            time_formatted_hour = input_time.strftime("%H:%M")
            
            current_time = datetime.now()
            time_difference = current_time - input_time
            seconds = time_difference.total_seconds()
            minutes = seconds / 60
            hours = minutes / 60
            time=""
            if hours>48:
                time=time_formated_day+" lúc "+time_formatted_hour
            elif hours<=48 and hours>=24:
                time="Hôm qua lúc "+time_formatted_hour 
            elif hours>=1 and hours<24:
                time=str(int(hours))+" giờ"
            elif minutes>0:
                time=str(int(minutes))+" phút"
            else:
                time="Vừa xong"
            post.set_time_post(time)
            print(time_difference.total_seconds())
            list_post_new.append(post)
        serializer = PostSerializer(list_post_new,many=True)
        return Response({"data":serializer.data,"message":"Success","code":200},status=status.HTTP_200_OK)
    serializer = PostSerializer(list_post_new,many=True)
    return Response({"data":serializer.data,"message":"Failded","code":400},status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_post(request,id_post):
    post=Post.objects.get(id_post=id_post)
    if post:
        images_to_delete = Image.objects.filter(post=post)
        images_to_delete.delete()
        comment_to_delete = Comment.objects.filter(post=post)
        comment_to_delete.delete()
        post.delete()
        return Response({"data":"","message":"Success","code":200},status=status.HTTP_200_OK)
    return Response({"data":"","message":"Failded","code":400},status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def post_detail(request,id_post):
    post=Post.objects.get(id_post=id_post)
    if post:
        specific_time = datetime.fromisoformat(str(post.time_post))
        time_string_without_offset = specific_time.strftime("%Y-%m-%d %H:%M:%S")
        input_time = datetime.strptime(time_string_without_offset, "%Y-%m-%d %H:%M:%S")
        time_formated_day = input_time.strftime("%d-%m-%Y")
        time_formatted_hour = input_time.strftime("%H:%M")
        
        current_time = datetime.now()
        time_difference = current_time - input_time
        seconds = time_difference.total_seconds()
        minutes = seconds / 60
        hours = minutes / 60
        time=""
        if hours>48:
            time=time_formated_day+" lúc "+time_formatted_hour
        elif hours<=48 and hours>=24:
            time="Hôm qua lúc "+time_formatted_hour 
        elif hours>=1 and hours<24:
            time=str(int(hours))+" giờ"
        elif minutes>0:
            time=str(int(minutes))+" phút"
        else:
            time="Vừa xong"
        post.set_time_post(time)
        serializer = PostSerializer(post)
        return Response({"data":serializer.data,"message":"Success","code":200},status=status.HTTP_200_OK)
    return Response({"data":"","message":"Failded","code":400},status=status.HTTP_400_BAD_REQUEST)