from django.shortcuts import render
from user_service.models import User
from .models import Comment
from post_service.models import Post 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import CommentSerializer
from rest_framework import status

# Create your views here.

@api_view(['POST'])
def add_comment(request,id_user,id_post):
    user=User.objects.get(id_user=id_user)
    post=Post.objects.get(id_post=id_post)
    data=request.GET
    if user and post:
        comment=Comment(
        time_cmt=data.get("time_cmt"),
        content=data.get("content"),
        user=user,
        post=post
        )
        comment.save()
        serializer = CommentSerializer(comment)
        return Response({"data":serializer.data,"message":"Success","code":200},status=status.HTTP_200_OK)
    return Response({"data":"","message":"Failded","code":400},status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_comment(request,id_comment):
    comment = Comment.objects.get(id_comment=id_comment)
    data=request.GET
    if comment:
        if data.get("content"):
            comment.set_content(data.get("content"))
        comment.save()
        serializer = CommentSerializer(comment)
        return Response({"data":serializer.data,"message":"Success","code":200},status=status.HTTP_200_OK)
    return Response({"data":"","message":"Failded","code":400},status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def all_comment(request,id_post):
    post=Post.objects.get(id_post=id_post)
    if post:
        list_comment=post.comment_set.all()
        serializer = CommentSerializer(list_comment,Many=True)
        return Response({"data":serializer.data,"message":"Success","code":200},status=status.HTTP_200_OK)
    return Response({"data":"","message":"Failded","code":400},status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_comment(request,id_comment):
    comment=Comment.objects.get(id_comment=id_comment)
    if comment:
        comment.delete()
        return Response({"data":"","message":"Success","code":200},status=status.HTTP_200_OK)
    return Response({"data":"","message":"Failded","code":400},status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def comment_detail(request,id_comment):
    comment=Comment.objects.get(id_comment=id_comment)
    if comment:
        serializer = CommentSerializer(comment)
        return Response({"data":serializer.data,"message":"Success","code":200},status=status.HTTP_200_OK)
    return Response({"data":"","message":"Failded","code":400},status=status.HTTP_400_BAD_REQUEST)