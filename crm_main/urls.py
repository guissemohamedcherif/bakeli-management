from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from apps.common import views
from django.views.static import serve
from django.conf.urls import url
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('admin/', admin.site.urls),

    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
    
  
    path('', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    path('base/',views.DashboardView.as_view(), name='base'),
    path('logout', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('users/',views.getUsers, name='userPage'),
    path('create-user',views.CreateUser.as_view(), name='userCreate'),
    path('create-members/',views.CreateMember, name='memberCreate'),
    path('delete-member/',views.deleteMember, name='memberDelete'),
    path(r'^member-update/(?P<id>\d+)/$', views.MemberUpdateView, name='MemberUpdate'),

]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
