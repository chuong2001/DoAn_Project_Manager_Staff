from django.shortcuts import render
from user_service.models import User
from .models import Comment,UserRead
from post_service.models import Post 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import CommentSerializer
from rest_framework import status
from datetime import datetime
from django.db.models import Q

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
        UserRead.objects.create(comment=comment,user=user)
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

@api_view(['DELETE'])
def delete_all_comment_user_in_post(request,id_user,id_post):
    user=User.objects.get(id_user=id_user)
    post=Post.objects.get(id_post=id_post)
    if user is not None and post is not None:
        listComment=Comment.objects.filter(Q(user=user) & Q(post=post))
        for comment in listComment:
            comment.delete();
        return Response({"data":"","message":"Success","code":200},status=status.HTTP_200_OK)
    return Response({"data":"","message":"Failded","code":400},status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def all_comment(request,id_post):
    post=Post.objects.get(id_post=id_post)
    data=request.GET
    if post:
        list_comment=Comment.objects.filter(post=post).order_by('-time_cmt')
        page=int(data.get('page'))
        size=int(data.get('size'))
        start=page
        end=page+size
        if end>len(list_comment): end=len(list_comment)
        list_comment=list_comment[start:end]
        serializer = CommentSerializer(list_comment,many=True)
        return Response({"data":serializer.data,"message":"Success","code":200},status=status.HTTP_200_OK)
    return Response({"data":"","message":"Failded","code":400},status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def check_read_comment(request,id_user,id_comment):
    comment=Comment.objects.get(id_comment=id_comment)
    if comment is not None:
        list_read=UserRead.objects.filter(comment=comment)
        if list_read is not None:
            for r in list_read:
                if id_user==r.user.id_user:
                    return Response({"data":"","message":"Success","code":200},status=status.HTTP_200_OK)
        return Response({"data":"","message":"Not found","code":404},status=status.HTTP_404_NOT_FOUND)
    return Response({"data":"","message":"Not found","code":404},status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def read_comment(request,id_user,id_post):
    post=Post.objects.get(id_post=id_post)
    listComment=Comment.objects.filter(post=post)
    user=User.objects.get(id_user=id_user)
    if post is not None and user is not None and listComment is not None:
        list_read=UserRead.objects.filter(user=user)
        if list_read is not None:
            for comment in listComment:
                check=False
                for read in list_read:
                    if read.comment.id_comment==comment.id_comment:
                        check=True
                        break
                if check==False:
                    UserRead.objects.create(user=user,comment=comment)
            return Response({"data":"","message":"Success","code":200},status=status.HTTP_200_OK)
    return Response({"data":"","message":"False","code":400},status=status.HTTP_400_BAD_REQUEST)


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