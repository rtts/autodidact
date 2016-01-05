from django.contrib import admin
from django.db import models
from django.forms import RadioSelect
from .models import *
from adminsortable.admin import SortableAdmin

@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    pass

class InlineSessionAdmin(admin.TabularInline):
    model = Session

@admin.register(Course)
class CourseAdmin(SortableAdmin):
    inlines = [InlineSessionAdmin]

@admin.register(Download)
class DownloadAdmin(admin.ModelAdmin):
    list_filter = ['session']

@admin.register(Activity)
class ActivityAdmin(SortableAdmin):
    list_filter = ['session']

@admin.register(CompletedActivity)
class CompletedActivityAdmin(admin.ModelAdmin):
    pass
