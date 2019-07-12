"""
Definition of urls for pakguru_site.
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from pakguru_app.models import Post

info_dict = {
    'queryset': Post.objects.filter(is_active=True),
    'date_field': 'target_date',
}

urlpatterns = [
    url(r'^admin/shell/', include('django_admin_shell.urls')),
    url(r'^', include('reference_data_app.urls')),
    url(r'^', include('frontend_app.urls')),
    path('admin/', admin.site.urls),


    # the sitemap
    path('sitemap.xml', sitemap,
         {'sitemaps': {'talkshows': GenericSitemap(info_dict, priority=0.6,
                       changefreq='never')}},
         name='django.contrib.sitemaps.views.sitemap'),

]
# https://stackoverflow.com/questions/9181047/django-static-files-development
# urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
