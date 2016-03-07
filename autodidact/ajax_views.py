from django.http import HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required

from .decorators import *
from .utils import *
from .models import *

@staff_member_required
@needs_course
@need_session
def progresses(request, course, session):
    pass
