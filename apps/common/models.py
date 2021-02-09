from django.db import models

class Poste(models.Model):
    
    STATUTS_ELMTS = (
        ('ACTIVE', 'active'),
        ('INACTIVE', 'inactive'),        
    )
    
    designation = models.CharField(max_length=250, blank=True)
    abrev = models.CharField(max_length=10, blank=True)
    description = models.TextField(blank=True)
    statut = models.CharField(max_length=8, choices=STATUTS_ELMTS, default='')
    created_on = models.DateTimeField(auto_now_add=True)
    
    
class Departement(models.Model):
    
    STATUTS_ELMTS = (
        ('ACTIVE', 'active'),
        ('INACTIVE', 'inactive'),        
    )
    
    code = models.CharField(max_length=100, blank=True)
    nom = models.CharField(max_length=250, blank=True)
    description = models.TextField(blank=True)
    statut = models.CharField(max_length=8, choices=STATUTS_ELMTS, default='')
    created_on = models.DateTimeField(auto_now_add=True)


class Employe(models.Model):
    
    STATUTS_ELMTS = (
        ('ACTIVE', 'active'),
        ('INACTIVE', 'inactive'),        
    )
    
    code = models.CharField(max_length=100, blank=True)
    nom = models.CharField(max_length=250, blank=True)
    telephone = models.CharField(max_length=10, blank=True)
    email = models.EmailField(max_length=200)
    statut = models.CharField(max_length=8, choices=STATUTS_ELMTS)
    poste = models.ForeignKey(Poste, on_delete=models.CASCADE,blank=True, null=True)
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE,blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    
    