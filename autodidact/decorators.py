from functools import wraps
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404, HttpResponseForbidden, HttpResponseBadRequest
from .models import *

def needs_course(view):
    @wraps(view)
    def wrapper(request, course_slug, *args, **kwargs):
        if isinstance(course_slug, Course):
            course = course_slug
        elif request.user.is_staff:
            course = get_object_or_404(Course, slug=course_slug)
        else:
            course = get_object_or_404(Course, slug=course_slug, active=True)
        return view(request, course, *args, **kwargs)
    return wrapper

def needs_session(view):
    @wraps(view)
    def wrapper(request, course, session_nr, *args, **kwargs):
        if not isinstance(course, Course):
            raise TypeError('Course object required')
        if isinstance(session_nr, Session):
            session = session_nr
        else:
            session_nr = int(session_nr)
            session = course.sessions.filter(number=session_nr).first()
            if session is None:
                raise Http404()
            if not session.active and not request.user.is_staff:
                raise Http404()
        return view(request, course, session, *args, **kwargs)
    return wrapper

def needs_assignment(view):
    @wraps(view)
    def wrapper(request, course, session, assignment_nr, *args, **kwargs):
        if not isinstance(course, Course):
            raise TypeError('Course object required')
        if not isinstance(session, Session):
            raise TypeError('Session object required')
        if isinstance(assignment_nr, Assignment):
            assignment = assignment_nr
        else:
            assignment_nr = int(assignment_nr)
            assignment = session.assignments.filter(number=assignment_nr).first()
            if assignment is None:
                raise Http404()
            if assignment.locked and not request.user.is_staff:
                if not request.user.attends.all() & session.classes.all():
                    return HttpResponseForbidden('Permission Denied')
            if not assignment.active and not request.user.is_staff:
                raise Http404()
        return view(request, course, session, assignment, *args, **kwargs)
    return wrapper

def needs_step(view):
    @wraps(view)
    def wrapper(request, course, session, assignment, *args, **kwargs):
        if not isinstance(course, Course):
            raise TypeError('Course object required')
        if not isinstance(session, Session):
            raise TypeError('Session object required')
        if not isinstance(assignment, Assignment):
            raise TypeError('Assignment object required')
        try:
            step = assignment.steps.filter(number=request.GET.get('step')).first()
            if step is None:
                return redirect(assignment.steps.first())
        except ValueError:
            return HttpResponseBadRequest('Invalid step number')
        return view(request, course, session, assignment, step, *args, **kwargs)
    return wrapper
