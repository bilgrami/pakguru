"""
Definition of urls for pakguru_site.
"""

from datetime import datetime

from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    url(r'^admin/shell/', include('django_admin_shell.urls')),
    url(r'^', include('pakguru_app.urls')),
    path('admin/', admin.site.urls),
]
# https://stackoverflow.com/questions/9181047/django-static-files-development
# urlpatterns += staticfiles_urlpatterns()
