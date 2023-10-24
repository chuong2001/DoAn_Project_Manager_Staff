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
from django.core.mail import send_mail
import random
import bcrypt
import string
from .jsonwebtokens import create_jwt,verify_jwt

def generate_random_code(length):
    characters = string.ascii_letters + string.digits
    code = ''.join(random.choice(characters) for i in range(length))
    return code

mainUrl='http:/192.168.11.103:8000/'

def checkAuthorization(request):
    authorization_header = request.META.get('HTTP_AUTHORIZATION')
    decoded_data=verify_jwt(authorization_header)
    if isinstance(decoded_data, dict)==False:
        return 1
    else:
        authorization=User.objects.get(id_user=decoded_data['data']['id_user'])
        if authorization is not None:
            return 0
    return 2

@api_view(['POST'])
def register_user(request):
    checkAu=checkAuthorization(request)
    if checkAu==0:
        data=request.GET
        avatar = data.get('avatar')
        birt=data.get('birthday')
        url_image=""
        if avatar is not None and len(avatar)>0:
            uploaded_file = request.FILES['image']
            with open('D:/DoAnTotNNghiep/ManagerStaff/media/' + uploaded_file.name, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            url_image='media/' +uploaded_file.name
        user=User(
        avatar=url_image,
        full_name=data.get('full_name'),
        birthday=data.get('birthday'),
        gender=data.get('gender'),
        address=data.get('address'),
        is_admin=0,
        email=data.get('email'),
        phone=data.get('phone'),
        wage=data.get('wage')
        )
        print(birt)
        date_object = datetime.strptime(birt, "%d-%m-%Y")
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
            return Response({"data":serializer.data,"message":"Success","code":201},status=status.HTTP_200_OK)
        else:
            serializer = UserSerializer(User())
            return Response({"data":serializer.data,"message":"Exist","code":400},status=status.HTTP_200_OK)
    elif checkAu==1:
        serializer = UserSerializer(User())
        return Response({"data":serializer.data,"message":"Expired","code":401},status=status.HTTP_200_OK)
    else:
        serializer = UserSerializer(User())
        return Response({"data":serializer.data,"message":"Failed","code":400},status=status.HTTP_200_OK)


@api_view(['GET'])
def user_detail(request,id_user):
    checkAu=checkAuthorization(request)
    if checkAu==0:
        user=User.objects.get(id_user=id_user)
        if user is not None:
            str_birthday=str(user.birthday)
            date_object = datetime.strptime(str_birthday, "%Y-%m-%d")
            new_date_string = date_object.strftime("%d-%m-%Y")    
            user.set_birthday(new_date_string)
            user.set_avatar(mainUrl+user.avatar)
            serializer = UserSerializer(user)
            return Response({"data":serializer.data,"message":"Success","code":200},status=status.HTTP_200_OK)
        else:
            serializer = UserSerializer(User())
            return Response({"data":serializer.data,"message":"Not Found","code":404},status=status.HTTP_200_OK)
    elif checkAu==1:
        serializer = UserSerializer(User())
        return Response({"data":serializer.data,"message":"Expired","code":401},status=status.HTTP_200_OK)
    else:
        serializer = UserSerializer(User())
        return Response({"data":serializer.data,"message":"Failed","code":400},status=status.HTTP_200_OK)
    
@api_view(['GET'])
def check_token(request):
    data=request.GET
    Authorization=data.get('Authorization')
    decoded_data = verify_jwt(Authorization)
    if isinstance(decoded_data, dict):
        user=User.objects.get(id_user=int(decoded_data['data']['id_user']))
        return Response({"data":str(decoded_data['data']['id_user'])+" "+str(user.is_admin),"message":"Success","code":200},status=status.HTTP_200_OK)
    else:
        return Response({"data":"","message":"Expired","code":401},status=status.HTTP_200_OK)

@api_view(['POST'])
def forgot_password(request):
    data=request.POST
    username=data.get('username')
    account=Account.objects.get(username=username)
    if account is not None:
        random_code = generate_random_code(6)
        subject = 'Mã xác minh email của bạn'
        message = random_code
        account.set_code(random_code)
        from_email = 'congtycnd01@gmail.com'
        recipient_list = [account.user.email]
        send_mail(subject, message, from_email, recipient_list)
        account.save()
        serializer = UserSerializer(account.user)
        return Response({"data":serializer.data,"message":"Success","code":201},status=status.HTTP_200_OK)
    serializer = UserSerializer(User())
    return Response({"data":serializer.data,"message":"Not found","code":404},status=status.HTTP_200_OK)

@api_view(['GET'])
def confirm_code_password(request,id_user):
    data=request.GET
    code=data.get('code')
    user=User.objects.get(id_user=id_user)
    print(user.email)
    if user is not None:
        account =Account.objects.get(user=user)
        print(account.code)
        print(code)
        if account is not None and account.code==code:
            return Response({"data":"","message":"Success","code":200},status=status.HTTP_200_OK)
    
    return Response({"data":"","message":"Not found","code":404},status=status.HTTP_200_OK)
            

@api_view(['GET'])
def get_code_user(request):
    data=request.GET
    username=data.get('username')
    account=Account.objects.get(username=username)
    if account is not None:
        return Response({"data":str(account.user.id_user)+"-"+str(account.user.full_name)+"-"+str(account.username),"message":"Success","code":200},status=status.HTTP_200_OK)
    return Response({"data":"","message":"Not exist","code":400},status=status.HTTP_200_OK)


@api_view(['GET'])
def login(request):
    data=request.GET
    username=data.get('username')
    password=data.get('password')
    listAccount=Account.objects.all()
    for account in listAccount:
        if account.username==username:
            if account.password==password:
                jwt_data=create_jwt({'id_user':account.user.id_user})
                return Response({"data":str(account.user.id_user)+" "+str(account.user.is_admin)+" "+jwt_data,"message":"Success","code":200},status=status.HTTP_200_OK)
            else:
                return Response({"data":"","message":"Failed","code":400},status=status.HTTP_200_OK)

    return Response({"data":"","message":"Not exist","code":400},status=status.HTTP_200_OK)
    
@csrf_exempt   
@api_view(['PUT'])
def update_user(request,id_user):
    checkAu=checkAuthorization(request)
    if checkAu==0:
        user=User.objects.get(id_user=id_user)
        data=request.GET
        if user is not None:
            account=Account.objects.get(user=user)
            avatar=data.get('avatar')
            avatar=avatar[len(mainUrl):len(avatar)]
            url_image=avatar
            if len(avatar)>0 and avatar!=user.avatar:
                try:
                    if os.path.exists(user.avatar):
                        os.remove('D:/DoAnTotNNghiep/ManagerStaff/'+user.avatar)
                    uploaded_file = request.FILES['image']
                    with open('D:/DoAnTotNNghiep/ManagerStaff/media/' + uploaded_file.name, 'wb+') as destination:
                        for chunk in uploaded_file.chunks():
                            destination.write(chunk)
                    url_image='media/' +uploaded_file.name
                except Exception as e:
                    serializer = UserSerializer(User())
                    return Response({"data":serializer.data,"message":"Failed","code":400},status=status.HTTP_200_OK)
        
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
            account.set_username(data.get('username'))
            account.set_password(data.get('password'))
            account.save()
            user.set_part(part)
            user.set_position(position)
            
            date_object = datetime.strptime(user.birthday, "%d-%m-%Y")
            new_date_string = date_object.strftime("%Y-%m-%d")
            user.set_birthday(new_date_string)
            user.save()
            serializer = UserSerializer(user)
            return Response({"data":serializer.data,"message":"Success","code":200},status=status.HTTP_200_OK)
        return Response({"data":"","message":"Not found","code":404},status=status.HTTP_200_OK)
    elif checkAu==1:
        serializer = UserSerializer(User())
        return Response({"data":serializer.data,"message":"Expired","code":401},status=status.HTTP_200_OK)
    else:
        serializer = UserSerializer(User())
        return Response({"data":serializer.data,"message":"Failed","code":400},status=status.HTTP_200_OK)


@api_view(['GET'])
def all_user(request):
    checkAu=checkAuthorization(request)
    if checkAu==0:
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
            listUserNew=[]
            for user in listUser:
                user.set_avatar(str(str(mainUrl)+str(user.avatar)))
                listUserNew.append(user)  
            serializer = UserSerializer(listUserNew,many=True)
            return Response({"data":serializer.data,"message":"Success","code":200},status=status.HTTP_200_OK)
        return Response({"data":[],"message":"Not found","code":404},status=status.HTTP_200_OK)
    elif checkAu==1:
        return Response({"data":[],"message":"Expired","code":401},status=status.HTTP_200_OK)
    else:
        return Response({"data":[],"message":"Failed","code":400},status=status.HTTP_200_OK)

@api_view(['GET'])
def all_part(request):
    checkAu=checkAuthorization(request)
    if checkAu==0:
        data = Part.objects.all()
        if data is not None:
            serializer = PartSerializer(data,many=True)
            return Response({"data":serializer.data,"message":"Success","code":200},status=status.HTTP_200_OK)
        return Response({"data":[],"message":"Not found","code":404},status=status.HTTP_200_OK)
    elif checkAu==1:
        return Response({"data":[],"message":"Expired","code":401},status=status.HTTP_200_OK)
    else:
        return Response({"data":[],"message":"Failed","code":400},status=status.HTTP_200_OK)


@api_view(['GET'])
def all_position_by_part(request,id_part):
    checkAu=checkAuthorization(request)
    if checkAu==0:
        part=Part.objects.get(id_part=id_part)
        if part is not None:
            data = PartDetail.objects.filter(part=part)
            if data:
                list=[]
                for d in data:
                    list.append(d.position)
                serializer = PositionSerializer(list,many=True)
                return Response({"data":serializer.data,"message":"Success","code":200},status=status.HTTP_200_OK)
        return Response({"data":[],"message":"Not found","code":404},status=status.HTTP_200_OK)
    elif checkAu==1:
        return Response({"data":[],"message":"Expired","code":401},status=status.HTTP_200_OK)
    else:
        return Response({"data":[],"message":"Failed","code":400},status=status.HTTP_200_OK)

@api_view(['GET'])
def get_part(request,id_part):
    checkAu=checkAuthorization(request)
    if checkAu==0:
        part=Part.objects.get(id_part=id_part)
        if part is not None:
            serializer=PartSerializer(part)
            return Response({"data":serializer.data,"message":"Success","code":200},status=status.HTTP_200_OK)
        serializer=PartSerializer(Part())
        return Response({"data":serializer.data,"message":"Not found","code":404},status=status.HTTP_200_OK)
    elif checkAu==1:
        serializer=PartSerializer(Part())
        return Response({"data":serializer.data,"message":"Expired","code":401},status=status.HTTP_200_OK)
    else:
        serializer=PartSerializer(Part())
        return Response({"data":serializer.data,"message":"Failed","code":400},status=status.HTTP_200_OK)


@api_view(['PUT'])
def change_password(request,id_user):
    checkAu=checkAuthorization(request)
    if checkAu==0:
        user=User.objects.get(id_user=id_user)
        account=Account.objects.get(user=user)
        data=request.GET
        if account is not None:
            if data.get("password"):
                password = data.get("password")
                account.set_password(password)
                account.save()
                serializer = UserSerializer(user)
                return Response({"data":serializer.data,"message":"Success","code":200},status=status.HTTP_200_OK)
        serializer = UserSerializer(user)
        return Response({"data":serializer.data,"message":"Not found","code":404},status=status.HTTP_200_OK)
    elif checkAu==1:
        serializer = UserSerializer(User())
        return Response({"data":serializer.data,"message":"Expired","code":401},status=status.HTTP_200_OK)
    else:
        serializer = UserSerializer(User())
        return Response({"data":serializer.data,"message":"Failed","code":400},status=status.HTTP_200_OK)


@api_view(['DELETE'])
def delete_user(request,id_user):
    checkAu=checkAuthorization(request)
    if checkAu==0:
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
    elif checkAu==1:
        return Response({"data":"","message":"Expired","code":401},status=status.HTTP_200_OK)
    else:
        return Response({"data":"","message":"Failed","code":400},status=status.HTTP_200_OK)
            