from django.shortcuts import render
from user_service.models import User
from .models import Feedback
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import FeedbackSerializer
from rest_framework import status

# Create your views here.

@api_view(['POST'])
def add_feedback(request,id_user):
    user=User.objects.get(id_user=id_user)
    data=request.GET
    if user:
        feedback=Feedback(
        time_feedback=data.get("time_feedback"),
        content=data.get("content"),
        is_read=1,
        user=user
        )
        feedback.save()
        return Response({"data":"","message":"Success","code":200},status=status.HTTP_200_OK)
    return Response({"data":"","message":"Failded","code":400},status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET'])
# def all_feedback(request,id_post):
#     post=Post.objects.get(id_post=id_post)
#     if post:
#         list_comment=post.comment_set.all()
#         serializer = CommentSerializer(list_comment,Many=True)
#         return Response({"data":serializer.data,"message":"Success","code":200},status=status.HTTP_200_OK)
#     return Response({"data":"","message":"Failded","code":400},status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_feedback(request,id_feedback):
    feedback=Feedback.objects.get(id_feedback=id_feedback)
    if feedback:
        feedback.delete()
        return Response({"data":"","message":"Success","code":200},status=status.HTTP_200_OK)
    return Response({"data":"","message":"Failded","code":400},status=status.HTTP_400_BAD_REQUEST)
