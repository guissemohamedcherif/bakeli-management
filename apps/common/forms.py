from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from apps.userprofile.models import Profile


class SignUpForm(UserCreationForm):
    
    first_name = forms.CharField(max_length=250, required = False, help_text = 'optional')
    last_name = forms.CharField(max_length=200, required = False, help_text = 'optional')
    email = forms.EmailField(max_length=254, help_text = 'valid email required')
     
    class Meta:
        model = User
        fields = [
            'username', 
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]
        

        
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username', 
            'first_name', 
            'last_name', 
            'email', 
        ]

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'bio',
            'tel',
            'birth_date',
            'profile_image'
        ]