from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
import django_cas as cas
import autodidact.urls

if settings.CAS_SERVER_URL:
    login_view = 'cas.views.login'
    logout_view = 'cas.views.logout'
else:
    login_view = 'django.contrib.auth.views.login'
    logout_view = 'django.contrib.auth.views.logout'

urlpatterns = [
    url(r'^login/$', login_view, name='login'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(autodidact.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
