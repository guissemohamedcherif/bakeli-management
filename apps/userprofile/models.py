from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
   
   
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True) 
    tel = models.CharField(max_length=15)
    adress = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
