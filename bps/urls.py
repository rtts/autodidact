import django.contrib.auth.views
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import autodidact.urls

def login(request):
    param = request.META['QUERY_STRING']
    return render(request, 'login.html', {
        'param': param,
    })

@login_required
def logout(request):
    if hasattr(request.user, 'uvt_user'):
        return redirect('logout_sso')
    else:
        return redirect('logout_regular')

urlpatterns = [
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^login/regular/$', django.contrib.auth.views.login, name='login_regular'),
    url(r'^logout/regular/$', django.contrib.auth.views.logout, name='logout_regular'),
]

if settings.CAS_SERVER_URL:
    import cas.views
    urlpatterns += [
        url(r'^login/sso/$',cas.views.login, name='login_sso'),
        url(r'^logout/sso/$',cas.views.logout, name='logout_sso'),
    ]

urlpatterns += [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(autodidact.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
