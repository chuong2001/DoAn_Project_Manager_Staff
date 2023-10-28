from django.db import models
from user_service.models import User
from post_service.models import Post

# Create your models here.
class NotificationPost(models.Model):
    id_notification=models.AutoField(primary_key=True)
    title_notification=models.CharField(max_length=250)
    body_notification=models.CharField(max_length=250)
    time_notification=models.DateTimeField()
    is_read=models.IntegerField()
    type_notification=models.IntegerField()
    id_data = models.IntegerField()
    user  =  models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    
    def set_id_notification(self, id_notification):
        self.id_notification = id_notification
        
    def set_title_notification(self, title_notification):
        self.title_notification = title_notification
        
    def set_body_notification(self, body_notification):
        self.body_notification = body_notification
        
    def set_time_notification(self, time_notification):
        self.time_notification = time_notification
        
    def set_type_notification(self, type_notification):
        self.type_notification = type_notification
        
    def set_is_read(self, is_read):
        self.is_read = is_read
        
    def set_id_data(self, id_data):
        self.id_data = id_data
        
    def set_user(self, user):
        self.user = user