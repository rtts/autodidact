from django.contrib import admin
from django.contrib import admin
from .models import *

@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    pass

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass
