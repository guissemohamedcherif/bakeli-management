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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class DashboardView(LoginRequiredMixin,TemplateView):
        template_name = 'base.html'  
        login_url = reverse_lazy('login') 


def getUsers(request):
    users = CustomUser.objects.exclude(tel = "771264968")
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
        stat1 = request.GET.get('stat', None)

        
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
        if stat1 == "1":
            user.stat = True
        else:
            user.stat = False
        
        user.save()
            
        
        user = {'id':obj.id,
                   'first_name':obj.first_name,
                   'last_name':obj.last_name,
                   'username':obj.username,
                   'email':obj.email,
                   'tel':obj.tel,
                   'adress':obj.adress,
                   'stat':obj.stat
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
        stat1 = request.GET.get('stat', None)
    
        
        obj = CustomUser.objects.get(id=id1)
        obj.first_name = prenom1
        obj.last_name = nom1
        obj.tel = tel1
        obj.adress = adress1
        obj.email = email1
        obj.username = username1
        if stat1 == "1":
            obj.stat = True
        else:
            obj.stat = False
        obj.password = make_password(pass1)

        obj.save()

        user = {'id':obj.id,'first_name':obj.first_name,'last_name':obj.last_name,'tel':obj.tel,'adress':obj.adress,'email':obj.email,'username':obj.username,'stat':obj.stat}

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


''' def CreateMember(request):
    persons = Person.objects.filter(stat=True)
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
'''

def deleteMember(request):
    id1 = request.GET.get('id', None)
    person = Person.objects.get(id=id1)
   
    if person.genre == "HOMME":
        pere = Pere.objects.get(person_id = person.id).delete()
      
        
    if person.genre == "FEMME":
        mere = Mere.objects.get(person_id = person.id).delete()
        
    person.delete()   
    data = {
            'deleted': True
        }
    return JsonResponse(data)


def MemberUpdateView(request):
    id1 = request.GET.get('id', None)
    obj = get_object_or_404(Person, id=id1)
    formedit = PersonForm()
    if request.method == "PUT":
        formedit = PersonForm(request.POST or None,request.FILES or None ,instance=obj)
        context ={'formedit':formedit}
        if formedit.is_valid():
            formedit.save()
    
    else :
        formedit = PersonForm()
        context = {}
            


def CreateMember(request):
    person_list = Person.objects.all()
    
    page = request.GET.get('page', 1)
 
    paginator = Paginator(person_list, 5)
    try:
        persons = paginator.page(page)
    except PageNotAnInteger:
        persons = paginator.page(1)
    except EmptyPage:
        persons = paginator.page(paginator.num_pages)
    return render(request, 'common/member.html',{'persons': persons}) 


def mCreate(request):
    if request.method == 'POST':
        if request.is_ajax():
            prenom = request.POST.get('formPrenom')
            nom = request.POST.get('formNom')
            tel = request.POST.get('formTel')
            genre = request.POST.get('formGenre')
            adress = request.POST.get('formAdress')
            image = request.FILES.get('formImage')
        
            if image:
            
                obj = Person.objects.create(
                    prenom=prenom,
                    nom = nom,
                    tel = tel,
                    genre = genre,
                    adress = adress, 
                    gene = 0,
                    image=image)
            else:
               obj = Person.objects.create(
                    prenom=prenom,
                    nom = nom,
                    tel = tel,
                    genre = genre,
                    gene = 0,
                    adress = adress) 
            
            obj2 = Person.objects.latest('id')
            
            enfant = Enfant.objects.create(
                person_id = obj2.id
            )
            if obj2.genre == "HOMME":
                pere = Pere.objects.create(
                    person_id = obj2.id
                )
            if obj2.genre == "FEMME":
                mere = Mere.objects.create(
                    person_id = obj2.id
                )
            
            person = {'id':obj.id,
                   'prenom':obj.prenom,
                   'nom':obj.nom,
                   'tel':obj.tel,
                   'genre':obj.genre,
                   'gene':obj.gene,
                   'adress':obj.adress,
                   'image':obj.image.url,    
                   }

            data = {
                'person': person
            }
            return JsonResponse(data)
        
         
def MemberEdit (request):
        
        if request.method == 'POST':
            if request.is_ajax():
                id1 = request.POST.get('formId')
                prenom = request.POST.get('formPrenom')
                nom = request.POST.get('formNom')
                tel = request.POST.get('formTel')
                genre = request.POST.get('formGenre')
                adress = request.POST.get('formAdress')
                image = request.FILES.get('formImage')
                
                obj = Person.objects.get(id=id1)
                obj.prenom = prenom
                obj.nom = nom
                obj.tel = tel
                obj.genre = genre
                obj.adress = adress
                
                if image:
                    obj.image = image
                obj.save()
                if image:
                    person = {
                        'id':obj.id,
                        'prenom':obj.prenom,
                        'nom':obj.nom,
                        'tel':obj.tel,
                        'genre':obj.genre,
                        'adress':obj.adress,
                        'image':obj.image.url     
                    }
                else:
                    person = {
                        'id':obj.id,
                        'prenom':obj.prenom,
                        'nom':obj.nom,
                        'tel':obj.tel,
                        'genre':obj.genre,
                        'adress':obj.adress,               
                    }
                data = {
                'person': person
            }
                return JsonResponse(data)
    
def linkParent(request,id):
    temlate = "common/linkToParent.html"
    niit = Person.objects.get(id=id)
    persons = Person.objects.exclude(id = id)
    context = {'niit':niit, 'persons':persons}
    return render(request,temlate,context)


def createLinkParent(request):
    id = request.GET.get('idPers', None)
    idP = request.GET.get('idPere', None)
    
    obj = Enfant.objects.get(person_id=id)
    if idP:
        person = Person.objects.get(id=idP)
        pere = Pere.objects.all()
        mere = Mere.objects.all()
        for pe in pere:
            if pe.person_id == person.id:
                obj.pere_id = pe.id
                enfPers = Person.objects.get(id=id)
                perePers = Person.objects.get(id=pe.person_id)
                if perePers.gene:
                    enfPers.gene = perePers.gene + 1 
                else:
                    enfPers.gene = enfPers.gene
                enfPers.save()
                obj.mere_id = None
        for me in mere :
            if me.person_id == person.id:
                obj.mere_id = me.id
                enfPers = Person.objects.get(id=id)
                merePers = Person.objects.get(id=me.person_id)
                if merePers.gene:
                    enfPers.gene = merePers.gene + 1
                else:
                    enfPers.gene = enfPers.gene
                enfPers.save()
                obj.pere_id = None
        if obj.person_id:
                obj.save()
    pers = {
        'id': obj.id
    }
    data = {
                'person': pers
            }
    return JsonResponse(data)
    
    
def mCreate2(request):
    if request.method == 'POST':
        if request.is_ajax():
            prenom = request.POST.get('formPrenom1')
            nom = request.POST.get('formNom1')
            tel = request.POST.get('formTel1')
            genre = request.POST.get('formGenre1')
            adress = request.POST.get('formAdress1')
            gene = request.POST.get('formGene1')
            image = request.FILES.get('formImage1')
            
            if image:
            
                obj = Person.objects.create(
                    prenom=prenom,
                    nom = nom,
                    tel = tel,
                    genre = genre,
                    adress = adress, 
                    gene = gene,
                    image=image)
            else:
               obj = Person.objects.create(
                    prenom=prenom,
                    nom = nom,
                    tel = tel,
                    genre = genre,
                    gene = gene,
                    adress = adress) 
            
            obj2 = Person.objects.latest('id')
            
            enfant = Enfant.objects.create(
                person_id = obj2.id
            )
            if obj2.genre == "HOMME":
                pere = Pere.objects.create(
                    person_id = obj2.id
                )
            if obj2.genre == "FEMME":
                mere = Mere.objects.create(
                    person_id = obj2.id
                )
            
            person = {'id':obj.id,
                   'prenom':obj.prenom,
                   'nom':obj.nom,
                   'tel':obj.tel,
                   'genre':obj.genre,
                   'adress':obj.adress,
                   'gene':obj.gene,
                   'image':obj.image.url,    
                   }

            data = {
                'person': person
            }
            return JsonResponse(data)
        
        
def MemberEdit2 (request):
        
        if request.method == 'POST':
            if request.is_ajax():
                id1 = request.POST.get('formId1')
                prenom = request.POST.get('formPrenom1')
                nom = request.POST.get('formNom1')
                tel = request.POST.get('formTel1')
                genre = request.POST.get('formGenre1')
                gene = request.POST.get('formGene1')
                adress = request.POST.get('formAdress1')
                image = request.FILES.get('formImage1')
                
                obj = Person.objects.get(id=id1)
                obj.prenom = prenom
                obj.nom = nom
                obj.tel = tel
                obj.genre = genre
                obj.adress = adress
                obj.gene = gene
                
                if image:
                    obj.image = image
                obj.save()
                if image:
                    person = {
                        'id':obj.id,
                        'prenom':obj.prenom,
                        'nom':obj.nom,
                        'tel':obj.tel,
                        'genre':obj.genre,
                        'gene':obj.gene,
                        'adress':obj.adress,
                        'image':obj.image.url     
                    }
                else:
                    person = {
                        'id':obj.id,
                        'prenom':obj.prenom,
                        'nom':obj.nom,
                        'tel':obj.tel,
                        'genre':obj.genre,
                        'gene':obj.gene,
                        'adress':obj.adress,               
                    }
                data = {
                'person': person
            }
                return JsonResponse(data)