from django.contrib import admin
from django.db import models
from django.forms import RadioSelect
from django.shortcuts import redirect
from .models import *
from adminsortable.admin import SortableAdmin, SortableStackedInline, SortableTabularInline

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

class InlineSessionAdmin(admin.StackedInline):
    model = Session

@admin.register(Course)
class CourseAdmin(FunkySaveAdmin, SortableAdmin):
    inlines = [InlineSessionAdmin]
    list_display = ['__unicode__', 'name', 'slug', 'url']
    list_filter = ['programmes']
    list_editable = ['name', 'slug']

class InlineAssignmentAdmin(SortableStackedInline):
    model = Assignment
    radio_fields = {'type': admin.HORIZONTAL}

class InlineDownloadAdmin(admin.StackedInline):
    model = Download
    extra = 1

class InlinePresentationAdmin(SortableStackedInline):
    model = Presentation
    extra = 1

class InlineClarificationAdmin(SortableStackedInline):
    model = Clarification
    extra = 1

@admin.register(Session)
class SessionAdmin(FunkySaveAdmin, SortableAdmin):
    def has_add_permission(self, request):
        return False
    inlines = [InlineDownloadAdmin, InlinePresentationAdmin, InlineAssignmentAdmin]
    list_filter = ['course']
    list_display = ['__unicode__', 'name', 'course', 'registration_enabled', 'active']
    list_editable = ['name', 'registration_enabled', 'active']
    exclude = ['course']

class InlineStepAdmin(SortableTabularInline):
    model = Step

@admin.register(Assignment)
class AssignmentAdmin(FunkySaveAdmin, SortableAdmin):
    def has_add_permission(self, request):
        return False
    inlines = [InlineStepAdmin]
    list_display = ['__unicode__', 'session', 'name', 'nr_of_steps', 'locked', 'active']
    list_filter = ['session__course', 'session']
    list_editable = ['name', 'locked', 'active']
    radio_fields = {'type': admin.HORIZONTAL}
    exclude = ['session']

@admin.register(Step)
class StepAdmin(FunkySaveAdmin, SortableAdmin):
    def has_add_permission(self, request):
        return False
    inlines = [InlineClarificationAdmin]
    list_display = ['__unicode__', 'description', 'answer_required', 'assignment']
    list_editable = ['answer_required']
    list_filter = ['assignment__session', 'assignment']
    exclude = ['assignment']

@admin.register(CompletedStep)
class CompletedStepAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False
    list_display = ['whom', 'step', 'date', 'answer']
    list_filter = ['step__assignment__session__course', 'whom']
    exclude = ['step', 'whom']

@admin.register(Download)
class DownloadAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False
    list_filter = ['session']
    list_display = ['__unicode__', 'session']
    exclude = ['session']

@admin.register(Presentation)
class PresentationAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False
    list_filter = ['session']
    list_display = ['__unicode__', 'session', 'visibility']
    radio_fields = {'visibility': admin.HORIZONTAL}
    exclude = ['session']

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False
    list_filter = ['session__course', 'session']
    list_display = ['number', 'session', 'ticket', 'nr_of_students']
    exclude = ['session']

@admin.register(Clarification)
class ClarificationAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False
    list_filter = ['step__assignment__session']
    list_display = ['__unicode__', 'step', 'description']
    exclude = ['step']
