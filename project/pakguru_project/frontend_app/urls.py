"""
Definition of urls for pakguru_site.
"""

from datetime import datetime
from django.contrib.auth.views import LoginView, LogoutView
from . import forms, views
from django.urls import path
# from django.conf.urls import url
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('dailytv/', views.dailytv, name='dailytv'),
    path('login/',
         LoginView.as_view
         (
             template_name='pakguru_app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Log in',
                 'year': datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]
# https://stackoverflow.com/questions/9181047/django-static-files-development
# urlpatterns += staticfiles_urlpatterns()
