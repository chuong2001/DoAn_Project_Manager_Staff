from django.shortcuts import render
from user_service.models import User
from .models import Comment
from post_service.models import Post 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import CommentSerializer
from rest_framework import status
from datetime import datetime

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
        specific_time = datetime.fromisoformat(str(comment.time_cmt))
        time_string_without_offset = specific_time.strftime("%Y-%m-%d %H:%M:%S")
        input_time = datetime.strptime(time_string_without_offset, "%Y-%m-%d %H:%M:%S")
        
        current_time = datetime.now()
        time_difference = current_time - input_time
        seconds = time_difference.total_seconds()
        minutes = seconds // 60
        hours = minutes // 60
        days=hours//24
        weeks=days//7
        months=days//30
        years=months//12
        time=""
        if years>0:
            time=str(years)+" năm"
        elif months>0:
            time=str(months)+" tháng"
        elif weeks>0:
            time=str(weeks)+" tuần"
        elif days>0:
            time=str(days)+" ngày"
        elif hours>=1 and hours<24:
            time=str(int(hours))+" giờ"
        elif minutes>0:
            time=str(int(minutes))+" phút"
        else:
            time="Vừa xong"
        comment.set_time_cmt(time)
        serializer = CommentSerializer(comment)
        return Response({"data":serializer.data,"message":"Success","code":200},status=status.HTTP_200_OK)
    serializer = CommentSerializer(Comment())
    return Response({"data":serializer.data,"message":"Failded","code":400},status=status.HTTP_400_BAD_REQUEST)


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