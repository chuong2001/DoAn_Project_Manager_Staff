from .models import Image,Post,TypePost
from comment_service.models import Comment
from rest_framework import serializers
from comment_service.serializer import CommentSerializer
from datetime import datetime

class TypePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypePost
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ("id_image","image")

class PostSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()  
    type_post = TypePostSerializer()
    comments = serializers.SerializerMethodField()  
    class Meta:
        model = Post
        fields = '__all__'

    def get_images(self, obj):
        images = Image.objects.filter(post=obj)
        return ImageSerializer(images, many=True).data
    
    def get_comments(self, obj):
        comments = Comment.objects.filter(post=obj)
        list_comments=[]
        for comment in comments:
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
                time=str(int(years))+" năm"
            elif months>0:
                time=str(int(months))+" tháng"
            elif weeks>0:
                time=str(int(weeks))+" tuần"
            elif days>0:
                time=str(int(days))+" ngày"
            elif hours>=1 and hours<24:
                time=str(int(hours))+" giờ"
            elif minutes>0:
                time=str(int(minutes))+" phút"
            else:
                time="Vừa xong"
            comment.set_time_cmt(time)
            list_comments.append(comment)
        return CommentSerializer(list_comments, many=True).data
     