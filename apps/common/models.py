from django.db import models
from apps.userprofile.models import CustomUser

class Person(models.Model):
    genre_stat = (
        ('HOMME', 'HOMME'),
        ('FEMME', 'FEMME'),        
    )
    prenom = models.CharField(max_length=250, blank=False)
    nom = models.CharField(max_length=250, blank=False)
    adress = models.TextField(blank=True, null=True)
    tel  = models.CharField(max_length=10, blank=False)
    genre = models.CharField(max_length=250, choices=genre_stat, default='')
    image = models.ImageField(default='users/login.png',upload_to='users/', null=True, blank=True)
    stat = models.BooleanField(default=True)
    gene =  models.IntegerField( blank=True, null=True)
    datenaiss = models.CharField(max_length=250, blank=True,null=True)
    lieunaiss = models.TextField(blank=True,null=True)
    datedeces = models.CharField(max_length=250, blank=True,null=True)
    lieudeces = models.TextField(blank=True,null=True)
    comment = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    

class Pere(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    stat = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    

class Mere(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    stat = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

class Enfant(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    pere = models.ForeignKey(Pere, on_delete=models.CASCADE,blank=True, null=True)
    mere = models.ForeignKey(Mere, on_delete=models.CASCADE,blank=True, null=True)
    stat = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)


class Annonces(models.Model):
    titre = models.CharField(max_length=250, blank=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)