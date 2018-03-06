import django.contrib.auth.views
from django.conf.urls import include, url
from django.contrib import admin
from .views import *

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', django.contrib.auth.views.login, name='login'),
    url(r'^logout/$', django.contrib.auth.views.logout, name='logout'),
    url(r'^$', homepage, name='homepage'),
    url(r'^doc/$', documentation, name='documentation'),
    url(r'^doc/([^/]+)/$', documentation, name='documentation'),
    url(r'^startclass/$', startclass, name='startclass'),
    url(r'^endclass/$', endclass, name='endclass'),
    url(r'^([^/]+)_courses/$', program, name='program'),
    url(r'^tag/([^/]+)/$', tag, name='tag'),

    url(r'^([^/]+)/$', course, name='course'),
    url(r'^([^/]+)/duplicate/$', copy_course, name='copy_course'),
    url(r'^([^/]+)/topic/([0-9]+)/$', topic, name='topic'),
    url(r'^([^/]+)/session/([0-9]+)/$', session, name='session'),
    url(r'^([^/]+)/session/([0-9]+)/print/$', print_session, name='print_session'),
    url(r'^([^/]+)/session/([0-9]+)/duplicate/$', copy_session, name='copy_session'),
    url(r'^([^/]+)/session/([0-9]+)/assignment/([0-9]+)/$', assignment, name='assignment'),
    url(r'^([^/]+)/session/([0-9]+)/students/$', progresses, name='progresses'),
    url(r'^([^/]+)/session/([0-9]+)/student/([^/]+)/$', progress, name='progress'),
    url(r'^([^/]+)/session/([0-9]+)/student/$', add_student, name='add_student'),
    url(r'^([^/]+)/session/([0-9]+)/student/([^/]+)/remove/$', remove_student, name='remove_student'),
    url(r'^([^/]+)/add_session/$', add_session, name='add_session'),
    url(r'^([^/]+)/session/([0-9]+)/add_assignment/$', add_assignment, name='add_assignment'),
    url(r'^([^/]+)/session/([0-9]+)/assignment/([0-9]+)/duplicate/$', copy_assignment, name='copy_assignment'),
#    url(r'^([^/]+)/quiz/$', quiz, name='quiz'),
    url(r'^([^/]+)/session/([0-9]+)/assignment/([0-9]+)/add_step/$', add_step, name='add_step'),
    url(r'^([^/]+)/session/([0-9]+)/assignment/([0-9]+)/delete_step/$', delete_step, name='delete_step'),
]
