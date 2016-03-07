from django.http import HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required

from .decorators import *
from .utils import *
from .models import *

@staff_member_required
@needs_course
@needs_session
def progresses(request, course, session):
    current_class = get_current_class(session, request.user)
    assignments = session.assignments.prefetch_related('steps')
    if current_class:
        students = current_class.students.all()
    else:
        students = []

    for s in students:
        (answers, progress) = calculate_progress(s, assignments)
        s.progress = progress
        s.answers = answers

    return render(request, 'autodidact/progresses.html', {
        'course': course,
        'session': session,
        'students': students,
    })
