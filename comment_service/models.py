from django.db import models
from post_service.models import Post
from user_service.models import User

# Create your models here.
class Comment(models.Model):
    id_comment=models.AutoField(primary_key=True)
    time_cmt=models.DateTimeField()
    content=models.TextField()
    post  =  models.ForeignKey(Post, null=True, on_delete=models.CASCADE,related_name='comments')
    user  =  models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.id_comment
    
    def set_id_comment(self, id_comment):
        self.id_comment = id_comment
        
    def set_time_cmt(self, time_cmt):
        self.time_cmt = time_cmt
        
    def set_content(self, content):
        self.content = content
        
class UserRead(models.Model):
    id_read=models.AutoField(primary_key=True)
    comment  =  models.ForeignKey(Comment, null=True, on_delete=models.CASCADE)
    user  =  models.ForeignKey(User, null=True, on_delete=models.CASCADE)
        
