from django.shortcuts import render
from .models import Post,Image
from user_service.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import PostSerializer
from rest_framework import status

# Create your views here.
@api_view(['POST'])
def add_post(request,id_user):
    data=request.GET
    user=User.objects.get(id_user=id_user)
    if user:
        post=Post(
        time_post=data.get("time_post"),
        content=data.get("content"),
        num_like=data.get("num_like"),
        num_comment=data.get("num_comment"),
        user=user)
        post.save()
        list_link_image=data.get("image").split()
        list_image=[]
        for link_image in list_link_image:
            image=Image.objects.create(image=link_image,post=post)
            list_image.append(image)

        # post_image_list=PostImageList(post=post,list_image=list_image)
        # serializer = PostImageListSerializer(post_image_list)
        return Response({"data":"","message":"Success","code":200},status=status.HTTP_200_OK)
    return Response({"data":"","message":"Failded","code":400},status=status.HTTP_400_BAD_REQUEST)
    