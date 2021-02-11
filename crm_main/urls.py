"""crm_main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from apps.common.views import HomeView,SignUpView,DashboardView,ProfileView,ProfileUpdateView
from apps.common.views import PosteView,CreatePoste,UpdatePoste
from django.contrib.auth import views as auth_views
from apps.common import views
from django.views.static import serve
from django.conf.urls import url
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name= 'home'),
    
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
    
    path('register/',SignUpView.as_view(), name='register'),
    
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    
    path('logout', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('base/',DashboardView.as_view(), name='base'),
    
    path('change-password', auth_views.PasswordChangeView.as_view(
        template_name = 'common/change-password.html', success_url ='/'), 
         name = 'change-password'),
    
    path('profile-update/', ProfileUpdateView.as_view(), name='profile-update'),
    path('profile/', ProfileView.as_view(), name='profile'),
    
    # Poste urls
    path('poste/', PosteView.as_view(), name='poste'),
    path('poste/create', views.CreatePoste.as_view(), name='poste_create'),
    path('poste/update', views.UpdatePoste.as_view(), name='poste_update'),
    path('poste/delete/',  views.DeletePoste.as_view(), name='poste_delete'),
    #End Poste urls
    
    # Departement urls
    path('departement/', views.DeptView.as_view(), name='dept'),
    path('departement/create', views.CreateDept.as_view(), name='dept_create'),
    path('departement/update', views.UpdateDept.as_view(), name='dept_update'),
    path('departement/delete/',  views.DeleteDept.as_view(), name='dept_delete'),
    
    # Employes urls
    path('getEmp/', views.getEmp, name='getEmp'),
    path('employe/create', views.CreateEmp.as_view(), name='emp_create'),
    path('employe/update', views.UpdateEmp.as_view(), name='emp_update'),
    path('employe/delete/',  views.DeleteEmp.as_view(), name='emp_delete'),

]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
