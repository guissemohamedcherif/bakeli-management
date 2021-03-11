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
import html.parser  
from .forms import PersonForm
from django.shortcuts import get_object_or_404


class DashboardView(LoginRequiredMixin,TemplateView):
        template_name = 'base.html'  
        login_url = reverse_lazy('login') 


def getUsers(request):
    users = CustomUser.objects.filter(stat=1)
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
                   'first_name':obj.first_name,
                   'last_name':obj.last_name,
                   'username':obj.username,
                   'email':obj.email,
                   'tel':obj.tel,
                   'adress':obj.adress
                   }

        data = {
            'user': user
        }
        return JsonResponse(data)
    

class UpdateUser(View):
    def  get(self, request):
        id1 = request.GET.get('id', None)
        nom1 = request.GET.get('nom', None)
        prenom1 = request.GET.get('prenom', None)
        tel1 = request.GET.get('tel', None)
        adress1 = request.GET.get('adress', None)
        email1 = request.GET.get('email', None)
        username1 = request.GET.get('username', None)
        pass1 = request.GET.get('password', None)
    
        
        obj = CustomUser.objects.get(id=id1)
        obj.first_name = prenom1
        obj.last_name = nom1
        obj.tel = tel1
        obj.adress = adress1
        obj.email = email1
        obj.username = username1
        obj.password = make_password(pass1)

        obj.save()

        user = {'id':obj.id,'first_name':obj.first_name,'last_name':obj.last_name,'tel':obj.tel,'adress':obj.adress,'email':obj.email,'username':obj.username}

        data = {
            'user': user
        }
        return JsonResponse(data)
    
    
def deleteUser(request):
    id = request.GET.get('id')
    user = CustomUser.objects.get(id=id)
    user.delete()
        
    data = {
            'deleted': True
        }
    return JsonResponse(data)


def CreateMember(request):
    persons = Person.objects.all()
    personform = PersonForm
    template_name = "common/member.html"
    if request.method == "POST":
        personform = PersonForm(request.POST,request.FILES)  
              
        if personform.is_valid():
            person = personform.save()
            
            obj = Person.objects.latest('id')
            
            enfant = Enfant.objects.create(
                person_id = obj.id
            )
            if obj.genre == "HOMME":
                pere = Pere.objects.create(
                    person_id = obj.id
                )
            if obj.genre == "FEMME":
                mere = Mere.objects.create(
                    person_id = obj.id
                )
            personform = PersonForm()
            return redirect('memberCreate')

    else:
        personform = PersonForm() 
    
    context = {'personform': personform, 'persons':persons} 
    return render (request,template_name,context)


def deleteMember(request):
    id1 = request.GET.get('id', None)
    person = Person.objects.get(id=id1)
    person.stat = False
    person.save()
    if person.genre == "HOMME":
        pere = Pere.objects.get(person_id = person.id)
        pere.stat = False
        pere.save()
        
    if person.genre == "FEMME":
        mere = Mere.objects.get(person_id = person.id)
        mere.stat = False
        mere.save()
        
    data = {
            'deleted': True
        }
    return JsonResponse(data)


def MemberUpdateView(request,id):
    obj = get_object_or_404(Person, id=id)
    
    form = PersonForm(request.POST or None,request.FILES or None ,instance=obj)
    if form.is_valid():
        form.save()
        return redirect('memberCreate')
    return render(request, 'common/editMember.html', {'form': form}) 