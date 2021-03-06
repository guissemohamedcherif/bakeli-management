from django.db import models
from apps.userprofile.models import CustomUser

class Person(models.Model):
    
    prenom = models.CharField(max_length=250, blank=False)
    nom = models.CharField(max_length=250, blank=False)
    adress = models.TextField(blank=False)
    tel  = models.CharField(max_length=10, blank=False)
    genre = models.CharField(max_length=250, blank=False)
    image = models.ImageField(default='login.png',upload_to='users/', null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    

class Pere(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE,blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    

class Mere(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE,blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)

class Enfant(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    pere = models.ForeignKey(Pere, on_delete=models.CASCADE,blank=True, null=True)
    mere = models.ForeignKey(Mere, on_delete=models.CASCADE,blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)

