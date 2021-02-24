from django.shortcuts import render
from django.views.generic import View, TemplateView, CreateView, ListView
from .forms import SignUpForm, UserForm, ProfileForm, EcoleForm
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from apps.userprofile.models import Profile, CustomUser
from apps.common.models import Ecole, Niveau, Classe, Eleve
from django.contrib import messages
from django.http import JsonResponse
from django.core import serializers
import json
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.views import PasswordChangeView


def HomeView(request,id):
    template_name = 'common/home.html'
    ecole = Ecole.objects.get(admin_id=id)
    classes = Classe.objects.all()
    listClass = []
    try:
        niveaux = Niveau.objects.filter(ecole_id= ecole.id)
    except Niveau.DoesNotExist:
        niveaux = None
    if niveaux:
       for classe in classes:
           for niveau in niveaux:
               if classe.niveau_id == niveau.id:
                   listClass.append(classe)
           
           
    countNiv = niveaux.count()
    countClss = len(listClass)
    context = {'countNiv': countNiv, 'countClss': countClss}
        
    return render(request,template_name, context)
 
class DashboardView(LoginRequiredMixin,TemplateView):
        template_name = 'base.html'  
        login_url = reverse_lazy('login') 


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'common/profile.html'

class ProfileUpdateView(LoginRequiredMixin, TemplateView):
    user_form = UserForm
    profile_form = ProfileForm
    template_name = 'common/profile-update.html'

    def post(self, request):

        post_data = request.POST or None
        file_data = request.FILES or None

        user_form = UserForm(post_data, instance=request.user)
        profile_form = ProfileForm(post_data, file_data, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully!')
            return HttpResponseRedirect(reverse_lazy('profile'))

        context = self.get_context_data(
                                        user_form=user_form,
                                        profile_form=profile_form
                                    )

        return self.render_to_response(context)     

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


#  ********* Users functions **********

def getUsers(request):
    users = User.objects.all()
    template = "admin/users.html"
    context = {"users":users}
    
    return render(request, template,context)
    
def deleteUser(request):
    id1 = request.GET.get('id', None)
    user = User.objects.get(id=id1)
    user.delete()
    data = {
            'deleted': True
        }
    return JsonResponse(data)


def InfoUserView(request, id= None):
    if id:
        user = User.objects.get(id=id)     
        return render (request, template_name= "admin/userInfos.html", context={'test': user})

class addPermission(View):
    def  get(self, request):
        id1 = request.GET.get('id', None)
        is_active1 = request.GET.get('is_active', None)
        is_admin = request.GET.get('is_admin', None)


        obj2 = User.objects.get(id=id1)
        if (is_active1 == "ACTIVE"):
            obj2.is_active = True
        elif (is_active1 == "INACTIVE"):
            obj2.is_active = False
            
        if(is_admin == "ACTIVE"):
            obj2.is_active = True
            obj2.is_staff = True
            obj2.is_superuser = True
        elif(is_admin == "INACTIVE"):
            obj2.is_staff = False
            obj2.is_superuser = False
           
        obj2.save()

class CreateUser(View):
    
    def  get(self, request):
        prenom1 = request.GET.get('prenom', None)
        nom1 = request.GET.get('nom', None)
        tel1 = request.GET.get('telephone', None)
        email1 = request.GET.get('email', None)
        username = request.GET.get('username', None)
        password1 = request.GET.get('password', None)
        role1 = request.GET.get('role', None)
        naissance1 = request.GET.get('naissance', None)
        
        obj = User.objects.create(
            first_name = prenom1,
            last_name = nom1,
            username = username,
            email = email1,
            password = password1
        )
        profile = Profile.objects.get(user_id = obj.id)
        profile.tel = tel1
        profile.naissance = naissance1
        profile.role = role1
        
        profile.save()
        
        user = User.objects.get(id = obj.id)
        if(role1 == "SUPER_ADMIN"):
             user.is_staff = True
             user.is_superuser = True
             user.save()
            
        
        user = {'id':obj.id,
                   'prenom':obj.prenom,
                   'nom':obj.nom,
                   'username':obj.username,
                   'email':obj.email,
                   'password':obj.password
                   }

        data = {
            'user': user
        }
        return JsonResponse(data)
    
def signup(request):

    if request.method == "POST":
        signup_form = SignUpForm(request.POST)
        profile_form = ProfileForm(request.POST)
        
        if signup_form.is_valid() and profile_form.is_valid():
            user = signup_form.save()
            
            obj = CustomUser.objects.latest('id')
            tel= profile_form.cleaned_data.get("tel")
            naissance= profile_form.cleaned_data.get("naissance")
            role = profile_form.cleaned_data.get("role")
            profile = Profile.objects.get(user_id=obj)
            profile.tel = tel
            profile.naissance = naissance
            profile.role = "ADMINISTRATEUR"
            profile.save() 
            
            ecole = Ecole.objects.create(
                admin_id = obj.id
            )

            messages.success(request, 'Vous vous inscrit avec success !')
            return redirect('login')


    else:
        signup_form = SignUpForm()
        profile_form = ProfileForm()
        ecoleform = EcoleForm()
    
    context = {'signup_form': signup_form, 'profile_form': profile_form} 
    return render (request, 'common/register.html',context)

        
class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'common/change-password.html'
    success_url = reverse_lazy('base')

    def form_valid(self, form):
        messages.success(self.request, 'Votre mot de passe a été modifié.')
        return super().form_valid(form)
    
    
def getSchool(request,id=None):
    
    try:
        ecole = Ecole.objects.get(admin_id = id)
    except:
        return redirect ('base')
    template_name = 'common/ecole.html'
    if ecole:
        
        context = {'ecole':ecole}
    else :
        context = {}
    return render(request, template_name, context)


def updateSchool(request,id=None):
    
    ecole = Ecole.objects.get(admin_id=id)
    formecole = EcoleForm(instance=ecole)
    if request.method == "POST":
        formecole = EcoleForm(request.POST)
        if formecole.is_valid():
            ecole.nom = formecole.cleaned_data.get("nom")
            ecole.tel = formecole.cleaned_data.get("tel")
            ecole.email = formecole.cleaned_data.get("email")
            ecole.adress = formecole.cleaned_data.get("adress")

            ecole.save()
            messages.success(request, 'Votre ecole a ete enregistrée avec success')
            return redirect('schoolProfile',id=id)

    context = {'formecole': formecole}
    return render(request, 'common/schoolUpdates.html', context)


def getNiveau(request,id=None):
    
    ecole = Ecole.objects.get(admin_id=id)
    template_name = 'ecole/niveau.html'
    try:
        niveaux = Niveau.objects.filter(ecole_id= ecole.id)
    except Niveau.DoesNotExist:
        niveaux = None
        
    context = {'niveaux': niveaux}
     
    return render(request,template_name,context)


def createNiveau(request,id=None):
    ecole = Ecole.objects.get(admin_id=id)
    nom1 = request.GET.get('nom', None)
    template = 'ecole/niveau.html'
    
    obj = Niveau.objects.create(
        nom = nom1,
        ecole = ecole
    )
    niveau = {'id':obj.id,
            'nom':obj.nom,
            'ecole': obj.ecole
                   }
    
    data = {
            'niveau': niveau
        }
    return JsonResponse(data)

class UpdateNiveau(View):
    def  get(self, request):
        id1 = request.GET.get('id', None)
        nom1 = request.GET.get('nom', None)
        
        obj = Niveau.objects.get(id=id1)
        obj.nom = nom1
        obj.save()

        niveau = {'id':obj.id,'nom':obj.nom,'ecole':obj.ecole.nom}

        data = {
            'niveau': niveau
        }
        return JsonResponse(data)

def deleteNiveau(request):
    id1 = request.GET.get('id', None)
    niveau = Niveau.objects.get(id=id1)
    niveau.delete()
    data = {
            'deleted': True
        }
    return JsonResponse(data)
         
    
def getClasse(request,id=None):
    template_name = 'ecole/classe.html'
    listclasse = []
    ecole = Ecole.objects.get(admin_id=id)
    classes = Classe.objects.all()
    id1 = ecole.id
    
    niveaux = Niveau.objects.filter(ecole_id= id1)
    if niveaux:
        for classe in classes:
            for niv in niveaux:
                if classe.niveau_id == niv.id:
                    listclasse.append(classe)
                
    context = {'list': listclasse, 'nivs':niveaux}
     
    return render(request,template_name,context)


def createClasse(request,id=None):

    nom1 = request.GET.get('nom', None)
    niveau1 =  request.GET.get('niveau', None)
    template = 'ecole/class.html'
    niv = Niveau.objects.get(id=niveau1)
    
    obj = Classe.objects.create(
        nom = nom1,
        niveau = niv,
    )
    classe = {
            'id':obj.id,
            'nom':obj.nom,
            'niveau': obj.niveau,
                   }
    
    data = {
            'classe': classe
        }
    return JsonResponse(data)

class UpdateClasse(View):
    def  get(self, request):
        id1 = request.GET.get('id', None)
        nom1 = request.GET.get('nom', None)
        niveau1 = request.GET.get('niveau', None)
        
        niveau = Niveau.objects.get(id=niveau1)


        obj = Classe.objects.get(id=id1)
        obj.nom = nom1
        obj.niveau = niveau
        obj.save()
        
        
def deleteClasse(request):
    id1 = request.GET.get('id', None)
    classe = Classe.objects.get(id=id1)
    classe.delete()
    data = {
            'deleted': True
        }
    return JsonResponse(data)


def getStudents(request,id):
    template_name = 'ecole/student.html' 
    ecole = Ecole.objects.get(admin_id=id)
    classes = Classe.objects.all()
    eleves = Eleve.objects.all()
    listclasse = []
    listStudents = []
    id1 = ecole.id
    
    niveaux = Niveau.objects.filter(ecole_id= id1)
    if niveaux:
        for classe in classes:
            for niv in niveaux:
                if classe.niveau_id == niv.id:
                    listclasse.append(classe)
    if listclasse:
        for elev in eleves:
            for clss in listclasse:
                if elev.classe_id == clss.id:
                    listStudents.append(elev)
                    
    context={'students': listStudents}
    return render(request,template_name,context)