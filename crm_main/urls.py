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
from apps.common.views import HomeView,DashboardView,ProfileView,ProfileUpdateView
from django.contrib.auth import views as auth_views
from apps.common import views
from django.views.static import serve
from django.conf.urls import url
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'^homePage/(?P<id>\d+)/$', views.HomeView, name= 'home'),

    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
    
    path('profile-update/', ProfileUpdateView.as_view(), name='profile-update'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('usercreation/', views.CreateUser.as_view(), name='createUser'),
    path('register/',views.signup, name='register'),

    path('', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),

    path('logout', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('base/',DashboardView.as_view(), name='base'),
    
    path('change-password', views.CustomPasswordChangeView.as_view(), 
         name = 'change-password'),
    
    # users urls
    path('getusers/', views.getUsers, name='getUsers'),
    path('getusers/delete', views.deleteUser, name='user_delete'),
    path(r'^userInfos/(?P<id>\d+)/$', views.InfoUserView, name='userInfo'),
    path('userInfos/useraddInfo/', views.addPermission.as_view(), name='userAddInfo'),
    
    # school urls
    path(r'^schools/(?P<id>\d+)/$', views.getSchool, name='schoolProfile'),
    path(r'^update/(?P<id>\d+)/$', views.updateSchool, name='schoolUpdate'),
    path(r'^niveaux/(?P<id>\d+)/$', views.getNiveau, name='allNiveaux'), 
    path(r'^niveau_create/(?P<id>\d+)/$', views.createNiveau, name='createNiveau'),  
    path('level-update', views.UpdateNiveau.as_view(), name='update_niveau'), 
    path('level-deleted', views.deleteNiveau, name='delete_niveau'),  
    
    path(r'^classes/(?P<id>\d+)/$', views.getClasse, name='allClasses'), 
    path(r'^classes-create/(?P<id>\d+)/$', views.createClasse, name='createClasses'),  
    path('classe-update', views.UpdateClasse.as_view(), name='update_classe'), 
    path('classe-deleted', views.deleteClasse, name='delete_classe'),  
    
    # Student urls
    path(r'^students/(?P<id>\d+)/$', views.getStudents, name='allStudents'), 

]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
