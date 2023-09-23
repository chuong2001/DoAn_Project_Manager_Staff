from django.db import models
from user_service.models import Part

# Create your models here.
class Calendar(models.Model):
    id_calendar=models.AutoField(primary_key=True)
    header_calendar=models.CharField(max_length=250)
    body_calendar=models.TextField()
    type_calendar=models.CharField(max_length=250)
    address=models.CharField(max_length=250)
    day_calendar=models.DateField()
    time_start=models.TimeField()
    time_end=models.TimeField()
    part  =  models.ForeignKey(Part, null=True, on_delete=models.CASCADE)

    def set_id_calendar(self, id_calendar):
        self.id_calendar = id_calendar

    def set_header_calendar(self, header_calendar):
        self.header_calendar = header_calendar

    def set_body_calendar(self, body_calendar):
        self.body_calendar = body_calendar

    def set_type_calendar(self, type_calendar):
        self.type_calendar = type_calendar

    def set_address(self, address):
        self.address = address
        
    def set_day_calendar(self, day_calendar):
        self.day_calendar = day_calendar

    def set_time_start(self, time_start):
        self.time_start = time_start

    def set_time_end(self, time_end):
        self.time_end = time_end

    def set_part(self, part):
        self.part = part