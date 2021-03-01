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
    
class Eleve(models.Model):
    prenom = models.CharField(max_length=250, blank=False)
    nom = models.CharField(max_length=250, blank=False)
    adresse = models.TextField() 
    tel = models.CharField(max_length=15, blank=False)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE,blank=True, null=True)
    ecole = models.ForeignKey(Ecole, on_delete=models.CASCADE,blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    


class Inscription(models.Model):
    num = models.IntegerField(max_length=25)
    date = models.CharField(max_length=250)
    montant = models.FloatField()
    eleve = models.ForeignKey(Eleve, on_delete=models.CASCADE,blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)

class Paiement(models.Model):
    montant = models.FloatField()
    date = models.CharField(max_length=250)
    inscription = models.ForeignKey(Inscription, on_delete=models.CASCADE,blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    
    