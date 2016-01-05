from django.shortcuts import render, get_object_or_404
from autodidact.models import *

def homepage(request):
    courses = Course.objects.all()
    return render(request, 'homepage.html', {
        'courses': courses,
    })

def course(request, slug):
    course = get_object_or_404(Course, slug=slug)
    courses = Course.objects.all()
    return render(request, 'course.html', {
        'course': course,
        'courses': courses,
    })
