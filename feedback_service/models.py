from django.db import models
from user_service.models import User

# Create your models here.
class Feedback(models.Model):
    id_feedback=models.AutoField(primary_key=True)
    time_feedback=models.DateTimeField()
    content=models.TextField()
    is_read=models.IntegerField()
    user  =  models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.id_feedback
    
    def set_id_feedback(self, id_feedback):
        self.id_feedback = id_feedback
        
    def set_time_feedback(self, time_feedback):
        self.time_feedback = time_feedback
        
    def set_content(self, content):
        self.content = content

    def set_is_read(self, is_read):
        self.is_read = is_read