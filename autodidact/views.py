from django.shortcuts import render, get_object_or_404
from autodidact.models import *

def homepage(request):
    programmes = Programme.objects.all()
    return render(request, 'homepage.html', {
        'programmes': programmes,
    })

def course(request, course):
    course = get_object_or_404(Course, slug=course)
    return render(request, 'course.html', {
        'course': course,
    })

def session(request, course, session_nr):
    session_nr = int(session_nr)
    course = get_object_or_404(Course, slug=course)
    session = course.sessions.all()[session_nr-1]
    return render(request, 'session.html', {
        'course': course,
        'session': session,
        'session_nr': session_nr,
    })

def assignment(request, course, session_nr, assignment_nr):
    session_nr = int(session_nr)
    assignment_nr = int(assignment_nr)
    course = get_object_or_404(Course, slug=course)
    session = course.sessions.all()[session_nr-1]
    assignment = session.assignments.all()[assignment_nr-1]
    return render(request, 'assignment.html', {
        'course': course,
        'session': session,
        'session_nr': session_nr,
        'assignment': assignment,
        'assignment_nr': assignment_nr,
    })
