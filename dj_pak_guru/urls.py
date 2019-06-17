"""
Definition of urls for dj_pak_guru.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views
from django.urls import include, path
from django.conf.urls import url


urlpatterns = [
    url(r'^admin/shell/', include('django_admin_shell.urls')),
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Log in',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
    path('hello/', include('hello.urls')),
    url(r'^', include('app.urls')),
]
# https://stackoverflow.com/questions/9181047/django-static-files-development
urlpatterns += staticfiles_urlpatterns()
