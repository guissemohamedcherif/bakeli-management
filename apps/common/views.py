from django.shortcuts import render
from django.views.generic import View, TemplateView, CreateView, ListView
from .forms import SignUpForm, UserForm
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from apps.userprofile.models import  CustomUser
from apps.common.models import  Person,Pere,Mere,Enfant
from django.contrib import messages
from django.http import JsonResponse
import json
from django.shortcuts import redirect
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import HttpResponse
from django.template.loader import get_template, render_to_string
from fpdf import FPDF, HTMLMixin
import html.parser    


class DashboardView(LoginRequiredMixin,TemplateView):
        template_name = 'base.html'  
        login_url = reverse_lazy('login') 


def getUsers(request):
    users = CustomUser.objects.all()
    template = "admin/users.html"
    context = {"users":users}
    return render(request, template,context)
    
class CreateUser(View):
    
    def  get(self, request):
        prenom1 = request.GET.get('prenom', None)
        nom1 = request.GET.get('nom', None)
        tel1 = request.GET.get('tel', None)
        adress1 = request.GET.get('adress', None)
        email1 = request.GET.get('email', None)
        username = request.GET.get('username', None)
        password1 = request.GET.get('password', None)
        
        obj = CustomUser.objects.create(
            first_name = prenom1,
            last_name = nom1,
            tel = tel1,
            adress = adress1,
            email = email1,
            username = username,
            password = make_password(password1)
        )
      
        
        user = CustomUser.objects.get(id = obj.id)   
        user.is_staff = True
        user.is_superuser = True
        user.save()
            
        
        user = {'id':obj.id,
                   'prenom':obj.prenom,
                   'nom':obj.nom,
                   'username':obj.username,
                   'email':obj.email,
                   'tel':obj.tel
                   }

        data = {
            'user': user
        }
        return JsonResponse(data)
    
    
def getMembers(request):
    persons = Person.objects.all()
    template = "common/membre.html"
    context = {"persons":persons}
    return render(request, template,context)