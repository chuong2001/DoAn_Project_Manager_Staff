from django.contrib import admin
from .models import User,Account,Position,Part,PartDetail

# Register your models here.
admin.site.register(Part)
admin.site.register(Position)
admin.site.register(PartDetail)
admin.site.register(User)
admin.site.register(Account)