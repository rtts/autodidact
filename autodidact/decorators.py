from functools import wraps
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponseForbidden
from .models import *

def needs_course(view):
    @wraps(view)
    def wrapper(request, course_slug, *args, **kwargs):
        if request.user.is_staff:
            course = get_object_or_404(Course, slug=course_slug)
        else:
            course = get_object_or_404(Course, slug=course_slug, active=True)
        return view(request, course, *args, **kwargs)
    return wrapper

def needs_session(view):
    @wraps(view)
    def wrapper(request, course, session_nr, *args, **kwargs):
        session_nr = int(session_nr)
        if session_nr < 1:
            raise Http404()
        try:
            session = course.sessions.all()[session_nr-1]
            session.nr = session_nr
        except IndexError:
            raise Http404()
        if not session.active and not request.user.is_staff:
            raise Http404()
        return view(request, course, session, *args, **kwargs)
    return wrapper

def needs_assignment(view):
    @wraps(view)
    def wrapper(request, course, session, assignment_nr, *args, **kwargs):
        assignment_nr = int(assignment_nr)
        try:
            assignment = session.assignments.all()[assignment_nr-1]
            assignment.nr = assignment_nr
        except IndexError:
            raise Http404()
        if assignment.locked and not request.user.is_staff:
            if not request.user.attends.all() & session.classes.all():
                return HttpResponseForbidden('Permission Denied')
        return view(request, course, session, assignment, *args, **kwargs)
    return wrapper
