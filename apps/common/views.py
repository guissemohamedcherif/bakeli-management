from django.shortcuts import render
from django.views.generic import View, TemplateView, CreateView, ListView
from .forms import SignUpForm, UserForm, ProfileForm
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from apps.userprofile.models import Profile
from django.contrib import messages
from apps.common.models import Poste,Departement, Employe
from django.http import JsonResponse
from django.core.serializers import serialize 
import json


class HomeView(TemplateView):
    template_name = 'common/home.html'
    
 
class DashboardView(LoginRequiredMixin,TemplateView):
        template_name = 'base.html'  
        login_url = reverse_lazy('home') 
    
class SignUpView(CreateView):
    
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'common/register.html'
    

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
    

class PosteView(ListView):
    model = Poste
    template_name = 'rh/poste.html'
    context_object_name = 'postes'
    
    

class CreatePoste(View):
    def  get(self, request):
        designation1 = request.GET.get('designation', None)
        abrev1 = request.GET.get('abrev', None)
        description1 = request.GET.get('description', None)
        statut1 = request.GET.get('statut', None)


        obj = Poste.objects.create(
            designation = designation1,
            abrev = abrev1,
            description = description1,
            statut = statut1
        )

        poste = {'id':obj.id,'designation':obj.designation,'abrev':obj.abrev,'description':obj.description,'statut':obj.statut}

        data = {
            'poste': poste
        }
        return JsonResponse(data)
    
    
class UpdatePoste(View):
    def  get(self, request):
        id1 = request.GET.get('id', None)
        designation1 = request.GET.get('designation', None)
        abrev1 = request.GET.get('abrev', None)
        description1 = request.GET.get('description', None)
        statut1 = request.GET.get('statut', None)

        obj2 = Poste.objects.get(id=id1)
        obj2.designation = designation1
        obj2.abrev = abrev1
        obj2.description = description1
        obj2.statut = statut1
        obj2.save()

        poste = {'id':obj2.id,'designation':obj2.designation,'abrev':obj2.abrev,'description':obj2.description,'statut':obj2.statut}

        data = {
            'poste': poste
        }
        return JsonResponse(data)
    
    
class DeletePoste(View):
    def  get(self, request):
        id1 = request.GET.get('id', None)
        Poste.objects.get(id=id1).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)

 # Departement function 
 
class DeptView(ListView):
        model = Departement
        template_name = 'rh/departement.html'
        context_object_name = 'departements'
    
    

class CreateDept(View):
    def  get(self, request):
        code1 = request.GET.get('code', None)
        nom1 = request.GET.get('nom', None)
        description1 = request.GET.get('description', None)
        statut1 = request.GET.get('statut', None)


        obj = Departement.objects.create(
            code = code1,
            nom = nom1,
            description = description1,
            statut = statut1
        )

        departement = {'id':obj.id,'code':obj.code,'nom':obj.nom,'description':obj.description,'statut':obj.statut}

        data = {
            'departement': departement
        }
        return JsonResponse(data)
    
    
class UpdateDept(View):
    def  get(self, request):
        id1 = request.GET.get('id', None)
        code1 = request.GET.get('code', None)
        nom1 = request.GET.get('nom', None)
        description1 = request.GET.get('description', None)
        statut1 = request.GET.get('statut', None)

        obj2 = Departement.objects.get(id=id1)
        obj2.code = code1
        obj2.nom = nom1
        obj2.description = description1
        obj2.statut = statut1
        obj2.save()

        departement = {'id':obj2.id,'code':obj2.code,'nom':obj2.nom,'description':obj2.description,'statut':obj2.statut}

        data = {
            'departement': departement
        }
        return JsonResponse(data)
    
    
class DeleteDept(View):
    def  get(self, request):
        id1 = request.GET.get('id', None)
        Departement.objects.get(id=id1).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)
    
# Employee class and function

class EmpView(ListView):
        model = Employe
        template_name = 'rh/employe.html'
        context_object_name = 'employes'
    

def getEmp(request):
            employes = Employe.objects.all()
            posts = Poste.objects.all()
            depts = Departement.objects.all()
        
            return render(request, template_name = "rh/employe.html",context = {"results":posts, "employes":employes,"depts":depts})
        
class CreateEmp(View):
    
    def  get(self, request):
        code1 = request.GET.get('code', None)
        nom1 = request.GET.get('nom', None)
        tel = request.GET.get('telephone', None)
        mail = request.GET.get('email', None)
        statut1 = request.GET.get('statut', None)
        poste1 = request.GET.get('poste', None)
        departement1 = request.GET.get('departement', None)
        
        post1 = Poste.objects.get(id=poste1)
        depart = Departement.objects.get(id=departement1)       

        obj = Employe.objects.create(
            code = code1,
            nom = nom1,
            telephone = tel,
            email = mail,
            statut = statut1,
            poste = post1,
            departement = depart
        )

        employe = {'id':obj.id,
                   'code':obj.code,
                   'nom':obj.nom,
                   'telephone':obj.telephone,
                   'email':obj.email,
                   'statut':obj.statut,
                   'poste':obj.poste,
                   'departement':obj.departement
                   }

        data = {
            'employe': employe
        }
        return JsonResponse(data)
    
class DeleteEmp(View):
    def  get(self, request):
        id1 = request.GET.get('id', None)
        Employe.objects.get(id=id1).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)
    
class UpdateEmp(View):
    def  get(self, request):
        id1 = request.GET.get('id', None)
        code1 = request.GET.get('code', None)
        nom1 = request.GET.get('nom', None)
        tel1 = request.GET.get('tel', None)
        email1 = request.GET.get('email', None)
        stat1 = request.GET.get('statut', None)
        poste1 = request.GET.get('poste', None)
        departement1 = request.GET.get('departement', None)
        
        post1 = Poste.objects.get(id=poste1)
        depart = Departement.objects.get(id=departement1)       


        obj2 = Employe.objects.get(id=id1)
        obj2.code = code1
        obj2.nom = nom1
        obj2.telephone = tel1
        obj2.email = email1
        obj2.statut = stat1
        obj2.poste = post1
        obj2.departement = depart
        obj2.save()

       
def searchDept(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        departements = Departement.objects.filter(
            code__istartswith=search_str) | Departement.objects.filter(
            nom__istartswith=search_str) | Departement.objects.filter(
            description__icontains=search_str) | Departement.objects.filter(
            statut__istartswith=search_str)
        
        data = departements.values()
        return JsonResponse(list(data), safe=False)
        
    