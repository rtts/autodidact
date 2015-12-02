from django.contrib import admin
from django.contrib import admin
from .models import *

@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    pass

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    pass

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    pass

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    pass

@admin.register(Completed)
class CompletedAdmin(admin.ModelAdmin):
    pass

