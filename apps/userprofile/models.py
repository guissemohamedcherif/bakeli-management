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

class Profile(models.Model):
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    tel = models.CharField(max_length=12, blank=True)
    naissance = models.CharField(max_length=100,blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

   # profile_image = models.ImageField(default='login.png',upload_to='users/', null=True, blank=True)
    
    def __str__(self):
        return '%s' % (self.user.username)

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()