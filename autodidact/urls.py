from django.conf.urls import include, url
from .views import *

urlpatterns = [
    url(r'^$', page, name='homepage'),
    url(r'^page/([^/]+)/$', page, name='page'),
    url(r'^startclass/$', startclass, name='startclass'),
    url(r'^endclass/$', endclass, name='endclass'),
    url(r'^([^/]+)/$', course, name='course'),
    url(r'^([^/]+)/topic/([0-9]+)/$', topic, name='topic'),
    url(r'^([^/]+)/session/([0-9]+)/$', session, name='session'),
    url(r'^([^/]+)/session/([0-9]+)/assignment/([0-9]+)/$', assignment, name='assignment'),
    url(r'^([^/]+)/session/([0-9]+)/students/$', progresses, name='progresses'),
    url(r'^([^/]+)/session/([0-9]+)/student/([^/]+)/$', progress, name='progress'),

    url(r'^([^/]+)/session/([0-9]+)/add/$', add_assignment, name='add_assignment'),
    url(r'^([^/]+)/session/([0-9]+)/assignment/([0-9]+)/add/$', add_step, name='add_step'),
]
