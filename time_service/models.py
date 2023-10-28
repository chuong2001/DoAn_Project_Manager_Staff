from django.db import models
from user_service.models import User

# Create your models here.
class TimeIn(models.Model):
    id_time_in=models.AutoField(primary_key=True)
    day_in=models.DateField()
    time_in=models.TimeField()
    user  =  models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    
    def set_day_in(self,day_in):
        self.day_in=day_in
    
    def set_time_in(self,time_in):
        self.time_in=time_in

    def set_user(self,user):
        self.user=user
    
    
class TimeOut(models.Model):
    id_time_out=models.AutoField(primary_key=True)
    day_out=models.DateField()
    time_out=models.TimeField()
    user  =  models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    
    def set_day_out(self,day_out):
        self.day_out=day_out
    
    def set_time_out(self,time_out):
        self.time_out=time_out
    
    def set_user(self,user):
        self.user=user