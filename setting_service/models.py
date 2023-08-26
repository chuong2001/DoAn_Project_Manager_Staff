from django.db import models

# Create your models here.
class Setting (models.Model):
    id_setting=models.AutoField(primary_key=True)
    time_start=models.TimeField()
    time_end=models.TimeField()
    overtime=models.FloatField()
    holiday=models.FloatField()
    day_off=models.FloatField()
    
    def set_time_start(self,time_start):
        self.time_start=time_start
    
    def set_time_end(self,time_end):
        self.time_end=time_end
        
    def set_overtime(self,overtime):
        self.overtime=overtime
        
    def set_holiday(self,holiday):
        self.holiday=holiday
        
    def set_day_off(self,day_off):
        self.day_off=day_off
