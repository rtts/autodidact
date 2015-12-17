from django.shortcuts import render
from django.http import HttpResponse

def itworks(request):
    return HttpResponse("It works!", content_type="text/plain")
