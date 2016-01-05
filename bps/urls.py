from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from autodidact import views

urlpatterns = [
    url(r'^$', views.homepage, name='homepage'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^([^/]+)/$', views.course, name='course'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
