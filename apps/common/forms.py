from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from apps.userprofile.models import CustomUser
from django.core.exceptions import ValidationError


class SignUpForm(UserCreationForm):
    
    first_name = forms.CharField(label="PRENOM", max_length=250)
    last_name = forms.CharField(label="NOM", max_length=200)
    tel = forms.CharField(label="TELEPHONE", max_length=15)
    adress = forms.CharField(label="ADRESSE",widget=forms.Textarea)
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
            'tel',
            'email',
            'adress',
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

        
class loginForm(forms.ModelForm):
        username = forms.CharField(label="NOM UTILISATEUR", max_length=250)
        password = forms.CharField(label="MOT DE PASSE", widget=forms.PasswordInput(),max_length=254)
        class Meta:
            model = CustomUser
            fields = [
            'username',
            'password',
            ]
            