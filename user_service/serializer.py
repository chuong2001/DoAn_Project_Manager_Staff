from .models import User,Account,Part,Position
from rest_framework import serializers
from time_service.serializer import TimeInSerializer,TimeOutSerializer
from time_service.models import TimeIn,TimeOut
from post_service.models import Post,Image
from post_service.serializer import PostSerializer
from comment_service.models import Comment
from comment_service.serializer import CommentSerializer
from datetime import datetime

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
        fields = ("id","username","password")

class UserSerializer(serializers.ModelSerializer):
    part = PartSerializer()
    position = PositionSerializer()
    account = serializers.SerializerMethodField()  
    time_ins =serializers.SerializerMethodField()  
    time_outs = serializers.SerializerMethodField()  
    posts =serializers.SerializerMethodField()  
    comments = serializers.SerializerMethodField()  
    class Meta:
        model = User
        fields = '__all__'

    def get_time_ins(self, obj):
        start_day = self.context.get('start_day')
        end_day = self.context.get('end_day')
        if start_day and end_day:
            time_ins = TimeIn.objects.filter(user=obj, day_in__range=(start_day, end_day))
        else:
            time_ins = TimeIn.objects.filter(user=obj)
        time_ins_fomat=[]
        for time in time_ins:
            str_time_date=str(time.day_in)
            date_object = datetime.strptime(str_time_date, "%Y-%m-%d")
            new_date_string = date_object.strftime("%d-%m-%Y")    
            time.set_day_in(new_date_string)
            time_ins_fomat.append(time)
        return TimeInSerializer(time_ins_fomat, many=True).data

    def get_time_outs(self, obj):
        start_day = self.context.get('start_day')
        end_day = self.context.get('end_day')
        
        if start_day and end_day:
            time_outs = TimeOut.objects.filter(user=obj, day_out__range=(start_day, end_day))
        else:
            time_outs = TimeOut.objects.filter(user=obj)
        time_outs_fomat=[]
        for time in time_outs:
            str_time_date=str(time.day_out)
            date_object = datetime.strptime(str_time_date, "%Y-%m-%d")
            new_date_string = date_object.strftime("%d-%m-%Y")    
            time.set_day_out(new_date_string)
            time_outs_fomat.append(time)    
        return TimeOutSerializer(time_outs_fomat, many=True).data

    
    def get_posts(self, obj):
        posts = Post.objects.filter(user=obj)
        return PostSerializer(posts, many=True).data
    
    # def get_account(self, obj):
    #     account = Account.objects.get(user=obj)
    #     return AccountSerializer(account).data
    
    def get_account(self, obj):
        if obj:
            try:
                account = Account.objects.get(user=obj)
                return AccountSerializer(account).data
            except Account.DoesNotExist:
                return AccountSerializer(Account()).data 
        return AccountSerializer(Account()).data
    
    def get_comments(self, obj):
        comments = Comment.objects.filter(user=obj)
        return CommentSerializer(comments, many=True).data

        