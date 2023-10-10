from django.shortcuts import render
from .models import User,Part,Position,Account,PartDetail
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import UserSerializer,AccountSerializer,PartSerializer,PositionSerializer
from rest_framework import status
from django.core.files import File
from ManagerStaff import settings
from time_service.models import TimeIn,TimeOut
from post_service.models import Post,Image
from comment_service.models import Comment
import os
from django.core.files.base import ContentFile
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
# Create your views here.

mainUrl='http:/192.168.1.9:8000/'

@api_view(['POST'])
def register_user(request):
    data=request.GET
    avatar = data.get('avatar')
    url_image=""
    if len(avatar)>0:
        uploaded_file = request.FILES['image']
        with open('D:/DoAnTotNNghiep/ManagerStaff/media/' + uploaded_file.name, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        url_image=mainUrl+'media/' +uploaded_file.name
    user=User(
    avatar=url_image,
    full_name=data.get('full_name'),
    birthday=data.get('birthday'),
    gender=data.get('gender'),
    address=data.get('address'),
    email=data.get('email'),
    phone=data.get('phone'),
    wage=data.get('wage')
    )
    date_object = datetime.strptime(str(user.birthday), "%d-%m-%Y")
    new_date_string = date_object.strftime("%Y-%m-%d")
    user.set_birthday(new_date_string)
    username=data.get('username')
    password=data.get('password')
    id_part=data.get('id_part')
    id_position=data.get('id_position')
    
    part=Part.objects.get(id_part=id_part)
    position=Position.objects.get(id_position=id_position)
    user.set_part(part)
    user.set_position(position)
    account_new=Account(username=username,password=password,user=user)
    check=True
    listAccount=Account.objects.all()
    for account in listAccount:
        if account.username==username:
            check=False
            break
    if check:
        user.save()
        account_new.save()
        serializer = UserSerializer(user)
        return Response({"data":serializer.data,"message":"Success","code":200},status=status.HTTP_201_CREATED)
    else:
        return Response({"data":"","message":"Failded","code":400},status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def user_detail(request,id_user):
    user=User.objects.get(id_user=id_user)
    if user is not None:
        str_birthday=str(user.birthday)
        date_object = datetime.strptime(str_birthday, "%Y-%m-%d")
        new_date_string = date_object.strftime("%d-%m-%Y")    
        user.set_birthday(new_date_string)
        serializer = UserSerializer(user)
        return Response({"data":serializer.data,"message":"Success","code":200},status=status.HTTP_200_OK)
    else:
        serializer = UserSerializer(User())
        return Response({"data":serializer.data,"message":"Not Found","code":404},status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def login(request):
   
    data=request.GET
    username=data.get('username')
    password=data.get('password')
    listAccount=Account.objects.all()
    for account in listAccount:
        if account.username==username:
            if account.password==password:
                serializer = UserSerializer(account.user)
                return Response({"data":serializer.data,"message":"Success","code":200},status=status.HTTP_200_OK)
            else:
                serializer = UserSerializer(User())
                return Response({"data":serializer.data,"message":"Wrong","code":400},status=status.HTTP_200_OK)
    serializer = UserSerializer(User())    
    return Response({"data":serializer.data,"message":"Not exist","code":404},status=status.HTTP_200_OK)
    
@csrf_exempt   
@api_view(['PUT'])
def update_user(request,id_user):
    user=User.objects.get(id_user=id_user)
    data=request.GET
    if user:
        avatar=data.get('avatar')
        url_image=""
        if len(avatar)>0:
            try:
                if os.path.exists(user.avatar):
                    os.remove('D:/DoAnTotNNghiep/ManagerStaff/media/'+user.avatar)
                uploaded_file = request.FILES['image']
                with open('D:/DoAnTotNNghiep/ManagerStaff/media/' + uploaded_file.name, 'wb+') as destination:
                    for chunk in uploaded_file.chunks():
                        destination.write(chunk)
                url_image=mainUrl+'media/' +uploaded_file.name
            except Exception as e:
                return Response({"data":"","message":"Failded","code":400},status=status.HTTP_400_BAD_REQUEST)
    
        user.set_avatar(url_image)
        if data.get('full_name'):
            user.set_full_name(data.get('full_name'))
        if data.get('birthday'):
            user.set_birthday(data.get('birthday'))
        if data.get('gender'):
            user.set_gender(data.get('gender'))
        if data.get('address'):
            user.set_address(data.get('address'))
        if data.get('email'):
            user.set_email(data.get('email'))
        if data.get('phone'):
            user.set_phone(data.get('phone'))
        if data.get('wage'):
            user.set_wage(data.get('wage'))
        
        id_part=data.get('id_part')
        id_position=data.get('id_position')
        part=Part.objects.get(id_part=id_part)
        position=Position.objects.get(id_position=id_position)
        user.set_part(part)
        user.set_position(position)
        date_object = datetime.strptime(user.birthday, "%d-%m-%Y")
        new_date_string = date_object.strftime("%Y-%m-%d")
        user.set_birthday(new_date_string)
        user.save()
        serializer = UserSerializer(user)
        return Response({"data":serializer.data,"message":"Success","code":200},status=status.HTTP_200_OK)
    return Response({"data":"","message":"Failded","code":400},status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def all_user(request):
    listUser = User.objects.all()
    data=request.GET
    if listUser is not None:
        listUser = [user for user in listUser if 'admin' not in Account.objects.get(user=user).username]
        page=int(data.get('page'))
        size=int(data.get('size'))
        keySearch=data.get('keysearch')
        if len(keySearch)>0:
            listUser = [user for user in listUser if keySearch.lower() in user.full_name.lower()]
        start=page
        end=page+size
        if end>len(listUser): end=len(listUser)
        listUser=listUser[start:end]
        serializer = UserSerializer(listUser,many=True)
        return Response({"data":serializer.data,"message":"Success","code":200},status=status.HTTP_200_OK)
    return Response({"data":"","message":"Failded","code":400},status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def all_part(request):
    data = Part.objects.all()
    if data:
        serializer = PartSerializer(data,many=True)
        return Response({"data":serializer.data,"message":"Success","code":200},status=status.HTTP_200_OK)
    return Response({"data":[],"message":"Failded","code":400},status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_part(request,id_user,id_part):
    data = Part.objects.get(id_part=id_part)
    if data:
        user=User.objects.get(id_user=id_user)
        if user:
            user.set_part(data)
            user.save()
            serializer = UserSerializer(user)
            return Response({"data":serializer.data,"message":"Success","code":200},status=status.HTTP_200_OK)
    serializer = UserSerializer(User())
    return Response({"data":serializer.data,"message":"Failded","code":400},status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_position(request,id_user,id_position):
    data = Position.objects.get(id_position=id_position)
    if data:
        user=User.objects.get(id_user=id_user)
        if user:
            user.set_position(data)
            user.save()
            serializer = UserSerializer(user)
            return Response({"data":serializer.data,"message":"Success","code":200},status=status.HTTP_200_OK)
    serializer = UserSerializer(User())
    return Response({"data":serializer.data,"message":"Failded","code":400},status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def all_position_by_part(request,id_part):
    part=Part.objects.get(id_part=id_part)
    if part:
        data = PartDetail.objects.filter(part=part)
        if data:
            list=[]
            for d in data:
                list.append(d.position)
            serializer = PositionSerializer(list,many=True)
            return Response({"data":serializer.data,"message":"Success","code":200},status=status.HTTP_200_OK)
    return Response({"data":[],"message":"Failded","code":400},status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_admin(request):
    data = Account.objects.all()
    if data:
        for account in data:
            if account.username=='admin':
                serializer = UserSerializer(account.user)
                return Response({"data":serializer.data,"message":"Success","code":200},status=status.HTTP_200_OK)
    serializer = UserSerializer(User())
    return Response({"data":serializer.data,"message":"Failded","code":400},status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_part(request,id_part):
    part=Part.objects.get(id_part=id_part)
    if part is not None:
        serializer=PartSerializer(part)
        return Response({"data":serializer.data,"message":"Success","code":200},status=status.HTTP_200_OK)
    serializer=PartSerializer(Part())
    return Response({"data":serializer.data,"message":"Failded","code":400},status=status.HTTP_400_BAD_REQUEST)


def save_image_to_media(uploaded_file):
    image_path = os.path.join('uploads', uploaded_file.name)
    full_image_path = os.path.join(settings.MEDIA_ROOT, image_path)

    with open(full_image_path, 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)
    return os.path.join(settings.MEDIA_URL, image_path)

@api_view(['PUT'])
def change_password(request,id_user):
    user=User.objects.get(id_user=id_user)
    account=Account.objects.get(user=user)
    data=request.GET
    if account:
        if data.get("password"):
            account.set_password(data.get("password"))
            account.save()
            serializer = UserSerializer(user)
            return Response({"data":serializer.data,"message":"Success","code":200},status=status.HTTP_200_OK)
    serializer = UserSerializer(user)
    return Response({"data":serializer.data,"message":"Failded","code":400},status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_user(request,id_user):
    user=User.objects.get(id_user=id_user)
    
    listTimeIn=TimeIn.objects.filter(user=user)
    listTimeOut=TimeOut.objects.filter(user=user)
    account=Account.objects.get(user=user)
    listPosts=Post.objects.filter(user=user)
    listComments=Comment.objects.filter(user=user)
        
    for timein in listTimeIn:
        timein.delete()
    
    for timeout in listTimeOut:
        timeout.delete()
        
    account.delete()
    
    for comment in listComments:
        comment.delete()
    
    for post in listPosts:
        listCmt=Comment.objects.filter(post=post)
        for comment in listCmt:
            comment.delete()
        listImg=Image.objects.filter(post=post)
        for img in listImg:
            img.delete()
            
    user.delete()
    
    return Response({"data":"","message":"Success","code":200},status=status.HTTP_200_OK)
            