from django.shortcuts import render
from .models import User,Part,Position,Account
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import UserSerializer,AccountSerializer
from rest_framework import status
import json
# Create your views here.

@api_view(['POST'])
def register_user(request):
    data=request.GET
    user=User(
    avatar=data.get('avatar'),
    full_name=data.get('full_name'),
    birthday=data.get('birthday'),
    gender=data.get('gender'),
    address=data.get('address'),
    email=data.get('email'),
    phone=data.get('phone'),
    wage=data.get('wage')
    )
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
        serializer = UserSerializer(user)
        return Response({"data":serializer.data,"message":"Success","code":200},status=status.HTTP_200_OK)
    else:
        return Response({"data":"","message":"Not Found","code":404},status=status.HTTP_404_NOT_FOUND)


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
                return Response({"data":"","message":"Wrong","code":400},status=status.HTTP_400_BAD_REQUEST)
            
    return Response({"data":"","message":"Not exist","code":404},status=status.HTTP_404_NOT_FOUND)
    
    
@api_view(['PUT'])
def update_user(request,id_user):
    user=User.objects.get(id_user=id_user)
    data=request.GET
    if user:
        if data.get('avatar'):
            user.set_avatar(data.get('avatar'))
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
        user.save()
        serializer = UserSerializer(user)
        return Response({"data":serializer.data,"message":"Success","code":200},status=status.HTTP_200_OK)
    return Response({"data":"","message":"Failded","code":400},status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def all_user(request):
    data = User.objects.all()
    if data:
        serializer = UserSerializer(data,many=True)
        return Response({"data":serializer.data,"message":"Success","code":200},status=status.HTTP_200_OK)
    return Response({"data":"","message":"Failded","code":400},status=status.HTTP_400_BAD_REQUEST)


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
    return Response({"data":"","message":"Failded","code":400},status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_user(request,id_user):
    listAccount=Account.objects.all()
    for account in listAccount:
        if account.user.id_user==id_user:
            account.delete()
            return Response({"data":"","message":"Success","code":200},status=status.HTTP_200_OK)
        
    return Response({"data":"","message":"Failded","code":400},status=status.HTTP_400_BAD_REQUEST)
            