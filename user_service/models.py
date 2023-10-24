from typing import Any
from django.db import models
import json
# Create your models here.

class Part(models.Model):
    id_part=models.AutoField(primary_key=True)
    name_part=models.CharField(max_length=250)
    describe_part=models.CharField(max_length=250)
    
    def __str__(self):
        return self.id_part
    
    def set_id_part(self, id_part):
        self.id_part = id_part
    
    def set_name_part(self,name_part):
        self.name_part=name_part
        
    def set_describe_part(self,describe_part):
        self.describe_part=describe_part

class Position(models.Model):
    id_position=models.AutoField(primary_key=True)
    name_position=models.CharField(max_length=250)
    describe_position=models.TextField()
    
    def __str__(self):
        return self.id_position
    
    def set_id_position(self, id_position):
        self.id_position = id_position
    
    def set_name_position(self,name_position):
        self.name_position=name_position
        
    def set_describe_position(self,describe_position):
        self.describe_position=describe_position

class PartDetail(models.Model):
    part  =  models.ForeignKey(Part, null=True, on_delete=models.CASCADE)
    position  =  models.ForeignKey(Position, null=True, on_delete=models.CASCADE)


class User(models.Model):
    id_user=models.AutoField(primary_key=True)
    avatar=models.TextField(null=True)
    full_name=models.CharField(max_length=250)
    birthday=models.DateField()
    is_admin=models.IntegerField()
    gender=models.CharField(max_length=250)
    address=models.CharField(max_length=250)
    email=models.EmailField()
    phone=models.CharField(max_length=250)
    wage=models.FloatField()
    part  =  models.ForeignKey(Part, null=True, on_delete=models.CASCADE)
    position  =  models.ForeignKey(Position, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.id_user
    
    def set_id_user(self, id_user):
        self.id_user = id_user
    
    def set_avatar(self, avatar):
        self.avatar = avatar
    
    def set_full_name(self, full_name):
        self.full_name = full_name
    
    def set_birthday(self, birthday):
        self.birthday = birthday
        
    def set_is_admin(self, is_admin):
        self.is_admin = is_admin
    
    def set_gender(self, gender):
        self.gender = gender
    
    def set_address(self, address):
        self.address = address
        
    def set_email(self, email):
        self.email = email
    
    def set_phone(self, phone):
        self.phone = phone
    
    def set_wage(self, wage):
        self.wage = wage
        
    def set_part(self, part):
        self.part = part
    
    def set_position(self, position):
        self.position = position


class Account(models.Model):
    username=models.CharField(max_length=250)
    password=models.CharField(max_length=250)
    code=models.CharField(max_length=250)
    key=models.TextField()
    user  =  models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def set_username(self, username):
        self.username = username
    
    def set_password(self, password):
        self.password = password
        
    def set_key(self, key):
        self.key = key
        
    def set_code(self, code):
        self.code = code
        
    def set_user(self, user):
        self.user = user
