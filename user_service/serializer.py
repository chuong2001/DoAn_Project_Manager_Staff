from .models import User,Account,Part,Position
from rest_framework import serializers
from time_service.serializer import TimeInSerializer,TimeOutSerializer
from time_service.models import TimeIn,TimeOut
from post_service.models import Post,Image
from post_service.serializer import PostSerializer
from comment_service.models import Comment
from comment_service.serializer import CommentSerializer

class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = '__all__'
    
class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ("username","password")

class UserSerializer(serializers.ModelSerializer):
    part = PartSerializer()
    position = PositionSerializer()
    account = AccountSerializer()
    time_ins = TimeInSerializer()
    time_outs = TimeOutSerializer()
    posts = PostSerializer()
    comments = CommentSerializer()
    class Meta:
        model = User
        fields = '__all__'

    def get_time_ins(self, obj):
        start_day = self.context.get('start_day')  
        end_day = self.context.get('end_day')      
        
        if start_day and end_day:
            time_ins = TimeIn.objects.filter(user=obj, day_in=(start_day, end_day))
        else:
            time_ins = TimeIn.objects.filter(user=obj)
            
        return TimeInSerializer(time_ins, many=True).data

    def get_time_outs(self, obj):
        start_day = self.context.get('start_day')
        end_day = self.context.get('end_day')
        
        if start_day and end_day:
            time_outs = TimeOut.objects.filter(user=obj, day_out=(start_day, end_day))
        else:
            time_outs = TimeOut.objects.filter(user=obj)
            
        return TimeOutSerializer(time_outs, many=True).data

    
    def get_posts(self, obj):
        posts = Post.objects.filter(user=obj)
        return PostSerializer(posts, many=True).data
    
    def get_comments(self, obj):
        comments = Comment.objects.filter(user=obj)
        return CommentSerializer(comments, many=True).data

        