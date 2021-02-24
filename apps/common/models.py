from django.db import models
from apps.userprofile.models import CustomUser

class Ecole(models.Model):
    
    nom = models.CharField(max_length=250, blank=False)
    email = models.EmailField(max_length=250, blank=False)
    adress = models.TextField(blank=False)
    tel  = models.CharField(max_length=10, blank=False)
    admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE,blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)

class Niveau(models.Model):
    nom = models.CharField(max_length=250, blank=False)
    ecole = models.ForeignKey(Ecole, on_delete=models.CASCADE,blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    
class Classe(models.Model):
    nom = models.CharField(max_length=250, blank=False)
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE,blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
