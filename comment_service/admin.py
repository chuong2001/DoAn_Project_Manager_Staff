from django.contrib import admin
from .models import Comment,UserRead

# Register your models here.
admin.site.register(Comment)
admin.site.register(UserRead)