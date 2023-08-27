from django.db import models
from user_service.models import User

class Post(models.Model):
    id_post=models.AutoField(primary_key=True)
    time_post=models.DateTimeField()
    content=models.TextField()
    num_like=models.IntegerField()
    num_comment=models.IntegerField()
    user  =  models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.id_post
    
    def set_id_post(self, id_post):
        self.id_post = id_post
    
    def set_time_post(self, time_post):
        self.time_post = time_post
    
    def set_content(self, content):
        self.content = content
    
    def set_num_like(self, num_like):
        self.num_like = num_like
    
    def set_num_comment(self, num_comment):
        self.num_comment = num_comment
    
class Image(models.Model):
    id_image=models.AutoField(primary_key=True)
    image=models.TextField()
    post  =  models.ForeignKey(Post, null=True, on_delete=models.CASCADE)

    def set_image(self, image):
        self.image=image