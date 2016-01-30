from django.contrib import admin
from django.db import models
from django.forms import RadioSelect
from django.shortcuts import redirect
from .models import *
from adminsortable.admin import SortableAdmin, SortableStackedInline

class FunkySaveAdmin(object):
    '''
    Redirects to the object on site when clicking the save button
    '''
    def response_add(self, request, obj, post_url_continue=None):
        if '_save' in request.POST:
            return redirect(obj.get_absolute_url())
        else:
            return super(FunkySaveAdmin, self).response_add(request, obj, post_url_continue)

    def response_change(self, request, obj):
        if '_save' in request.POST:
            return redirect(obj.get_absolute_url())
        else:
            return super(FunkySaveAdmin, self).response_change(request, obj)

    save_on_top = True

@admin.register(Programme)
class ProgrammeAdmin(admin.ModelAdmin):
    pass

class InlineSessionAdmin(admin.TabularInline):
    model = Session

@admin.register(Course)
class CourseAdmin(FunkySaveAdmin, SortableAdmin):
    inlines = [InlineSessionAdmin]

class InlineAssignmentAdmin(SortableStackedInline):
    model = Assignment

class InlineDownloadAdmin(admin.StackedInline):
    model = Download.session.through

@admin.register(Session)
class SessionAdmin(FunkySaveAdmin, SortableAdmin):
    inlines = [InlineDownloadAdmin, InlineAssignmentAdmin]

class InlineActivityAdmin(SortableStackedInline):
    model = Activity

@admin.register(Assignment)
class AssignmentAdmin(FunkySaveAdmin, SortableAdmin):
    inlines = [InlineActivityAdmin]
    list_filter = ['session__course']

@admin.register(Activity)
class ActivityAdmin(FunkySaveAdmin, SortableAdmin):
    pass

@admin.register(CompletedActivity)
class CompletedActivityAdmin(admin.ModelAdmin):
    pass

@admin.register(Download)
class DownloadAdmin(admin.ModelAdmin):
    list_filter = ['session']

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_filter = ['session']
