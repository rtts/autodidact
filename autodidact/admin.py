from django.contrib import admin
from django.db import models
from django.forms import RadioSelect
from .models import *
from adminsortable.admin import SortableAdmin, SortableStackedInline

@admin.register(Programme)
class ProgrammeAdmin(admin.ModelAdmin):
    pass

class InlineSessionAdmin(admin.TabularInline):
    model = Session

@admin.register(Course)
class CourseAdmin(SortableAdmin):
    inlines = [InlineSessionAdmin]

class InlineActivityAdmin(SortableStackedInline):
    model = Activity

@admin.register(Assignment)
class AssignmentAdmin(SortableAdmin):
    inlines = [InlineActivityAdmin]
    list_filter = ['session__course']

@admin.register(CompletedActivity)
class CompletedActivityAdmin(admin.ModelAdmin):
    pass

@admin.register(Download)
class DownloadAdmin(admin.ModelAdmin):
    list_filter = ['session']
