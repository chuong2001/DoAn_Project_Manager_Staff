from django.shortcuts import render
from .models import Post,Image,TypePost
from comment_service.models import Comment
from user_service.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import PostSerializer,TypePostSerializer
from rest_framework import status
from datetime import datetime
from django.db.models import Max
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import os
import pytz

mainUrl='http:/192.168.11.103:8000/'

# Create your views here.
@api_view(['POST'])
def add_post(request,id_user):
    data=request.GET
    user=User.objects.get(id_user=id_user)
    if user:
        id_type_post=data.get("id_type_post")
        typePost=TypePost.objects.get(id_type=id_type_post)
        post=Post(
        type_post=typePost,
        header_post=data.get("header_post"),
        time_post=data.get("time_post"),
        content=data.get("content"),
        num_like=data.get("num_like"),
        num_comment=data.get("num_comment"),
        user=user)
        post.save()
        serializer = PostSerializer(post)
        return Response({"data":serializer.data,"message":"Success","code":200},status=status.HTTP_200_OK)
    serializer = PostSerializer(Post())
    return Response({"data":serializer.data,"message":"Failded","code":400},status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['PUT'])
def update_post(request,id_post):
    data=request.GET
    post=Post.objects.get(id_post=id_post)
    if post is not None:
        id_type_post=data.get("id_type_post")
        typePost=TypePost.objects.get(id_type=id_type_post)
        post.set_type_post(typePost)
        header_post=data.get("header_post")
        post.set_header_post(header_post)
        content=data.get("content")
        post.set_content(content)
        post.save()
        images_to_delete = Image.objects.filter(post=post)
        list_link_image=data.get("image").split()
        for image in images_to_delete:
            check=True
            for link_image in list_link_image:
                if image.image==link_image:
                    check=False
                    break
            if check==True and os.path.exists(image.image):
                os.remove('D:/DoAnTotNNghiep/ManagerStaff/media/'+image.image)
        
        images_to_delete.delete()
        serializer = PostSerializer(post)
        return Response({"data":serializer.data,"message":"Success","code":200},status=status.HTTP_200_OK)
    serializer = PostSerializer(Post())
    return Response({"data":serializer.data,"message":"Failded","code":400},status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def upload_image(request,id_post):
    if request.method == 'POST':
        post=Post.objects.get(id_post=id_post)
        uploaded_file = request.FILES['image']
        with open('D:/DoAnTotNNghiep/ManagerStaff/media/' + uploaded_file.name, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        url_image=mainUrl+'media/' +uploaded_file.name
        Image.objects.create(image=url_image,post=post)
        return JsonResponse({"data":url_image,"message":"Success","code":200},status=status.HTTP_200_OK)
    else:
        return JsonResponse({"data":"","message":"False","code":400}, status=400)


@api_view(['GET'])
def all_post(request):
    list_post=Post.objects.all().order_by('-time_post')
    list_post_new=[]
    data=request.GET
    if list_post is not None:
        page=int(data.get('page'))
        size=int(data.get('size'))
        keySearch=data.get('keysearch')
        filterTimeStart=data.get('time_start')
        filterTimeEnd=data.get('time_end')
        idTypePost=int(data.get('id_type_post'))
        
        if len(filterTimeStart)>0 and len(filterTimeEnd)>0:
            timestart = datetime.strptime(filterTimeStart, '%Y-%m-%d')
            timeend = datetime.strptime(filterTimeEnd, '%Y-%m-%d')
            list_post = list_post.filter(time_post__date__gte=timestart.date(), time_post__date__lte=timeend.date())
        
        if idTypePost>0:
            list_post = [post for post in list_post if idTypePost== post.type_post.id_type]
        
        if len(keySearch)>0:
            list_post = [post for post in list_post if keySearch.lower() in post.header_post.lower()]
        start=page
        end=page+size
        if end>len(list_post): end=len(list_post)
        list_post=list_post[start:end]
        for post in list_post:
            specific_time = datetime.fromisoformat(str(post.time_post))
            time_string_without_offset = specific_time.strftime("%Y-%m-%d %H:%M:%S")
            input_time = datetime.strptime(time_string_without_offset, "%Y-%m-%d %H:%M:%S")
            time_formated_day = input_time.strftime("%d-%m-%Y")
            time_formatted_hour = input_time.strftime("%H:%M")
            
            current_time = datetime.now()
            time_difference = current_time - input_time
            seconds = time_difference.total_seconds()
            minutes = seconds // 60
            hours = minutes // 60
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
            list_post_new.append(post)
        serializer = PostSerializer(list_post_new,many=True)
        return Response({"data":serializer.data,"message":"Success","code":200},status=status.HTTP_200_OK)
    return Response({"data":[],"message":"Success","code":200},status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def all_post_cmt(request):
    
    posts_with_latest_comment_time = Post.objects.annotate(
    latest_comment_time=Max('comments__time_cmt')
    )
    list_post = posts_with_latest_comment_time.order_by('-latest_comment_time')
    list_post_new=[]
    if list_post is not None:
        for post in list_post:
            specific_time = datetime.fromisoformat(str(post.time_post))
            time_string_without_offset = specific_time.strftime("%Y-%m-%d %H:%M:%S")
            input_time = datetime.strptime(time_string_without_offset, "%Y-%m-%d %H:%M:%S")
            time_formated_day = input_time.strftime("%d-%m-%Y")
            time_formatted_hour = input_time.strftime("%H:%M")
            
            current_time = datetime.now()
            time_difference = current_time - input_time
            seconds = time_difference.total_seconds()
            minutes = seconds // 60
            hours = minutes // 60
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
            list_post_new.append(post)
        serializer = PostSerializer(list_post_new,many=True)
        return Response({"data":serializer.data,"message":"Success","code":200},status=status.HTTP_200_OK)
    return Response({"data":[],"message":"Success","code":200},status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def all_type_post(request):
    list_type_post=TypePost.objects.all()
    if list_type_post:
        serializer = TypePostSerializer(list_type_post,many=True)
        return Response({"data":serializer.data,"message":"Success","code":200},status=status.HTTP_200_OK)
    return Response({"data":[],"message":"Success","code":200},status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_post(request,id_post):
    post=Post.objects.get(id_post=id_post)
    if post:
        images_to_delete = Image.objects.filter(post=post)
        for image in images_to_delete:
            image.delete()
        comment_to_delete = Comment.objects.filter(post=post)
        for comment in comment_to_delete:
            comment.delete()
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