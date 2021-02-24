from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from apps.userprofile.models import Profile, CustomUser
from django.core.exceptions import ValidationError
from .models import Ecole


class SignUpForm(UserCreationForm):
    
    first_name = forms.CharField(label="PRENOM", max_length=250)
    last_name = forms.CharField(label="NOM", max_length=200)
    email = forms.EmailField(label="EMAIL", max_length=254)
    password1 = forms.CharField(label="MOT DE PASSE", widget=forms.PasswordInput(),max_length=254)
    password2 = forms.CharField(label="CONFIRMEZ MOT DE PASSE", widget=forms.PasswordInput(),max_length=254)
    username = forms.CharField(label="NOM UTILISATEUR",max_length=254)


    class Meta:
        model = CustomUser
        fields = [
            'username', 
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]
    
    def getDuplicateEmail(self): 
        mail = self.cleaned_data.get('email')        
        for instance in CustomUser.object.all():
            if instance.email == mail:
                raise forms.ValidationError('Cet adresse email existe deja !')
            return mail
            
 

        
class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'username', 
            'first_name', 
            'last_name', 
            'email', 
        ]

class DateInput(forms.DateInput):
    input_type = 'date'

class ProfileForm(forms.ModelForm):
    tel = forms.CharField(
        label='TELEPHONE',
    )

    class Meta:
        model = Profile
        fields = [
            'tel',
            'naissance',
        ]
        widgets = {'naissance': DateInput(format='%d/%m/%Y')}

        
class loginForm(forms.ModelForm):
        class Meta:
            model = CustomUser
            fields = [
            'username',
            'password',
            ]
            

class EcoleForm(forms.ModelForm):
    
    nom = forms.CharField(label="NOM DE L'ECOLE", max_length=250)
    email = forms.EmailField(label="EMAIL", max_length=250)
    adress = forms.CharField(label="ADRESSE",widget=forms.Textarea)
    tel = forms.CharField(label="NUMERO TELEPHONE", max_length=10)


    class Meta:
        model = Ecole
        fields = [
            'nom', 
            'email',
            'adress',
            'tel',
        ]
    
    def getDuplicateEmail(self): 
        mail = self.cleaned_data.get('email')        
        for instance in Ecole.object.all():
            if instance.email == mail:
                raise forms.ValidationError('Adresse email deja existent !')
            return mail
        
    def getDuplicateNom(self): 
        nom = self.cleaned_data.get('nom')        
        for instance in Ecole.object.all():
            if instance.nom == nom:
                raise forms.ValidationError('Ce nom existe deja !')
            return nom
            
