from django.conf.urls import include, url
from .views import *
from .ajax_views import *

urlpatterns = [
    url(r'^$', homepage, name='homepage'),
    url(r'^startclass/$', startclass, name='startclass'),
    url(r'^endclass/$', endclass, name='endclass'),
    url(r'^([^/]+)/$', course, name='course'),
    url(r'^([^/]+)/session/([0-9]+)/$', session, name='session'),
    url(r'^([^/]+)/session/([0-9]+)/assignment/([0-9]+)/$', assignment, name='assignment'),
    url(r'^([^/]+)/session/([0-9]+)/student/([^/]+)/$', progress, name='progress'),
    url(r'^([^/]+)/session/([0-9]+)/progresses/$', progresses, name='progresses'),
]
