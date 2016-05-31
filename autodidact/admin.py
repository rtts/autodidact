from django.contrib import admin
from django.db import models
from django.forms import RadioSelect
from django.shortcuts import redirect
from .models import *

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

@admin.register(Page)
class PageAdmin(FunkySaveAdmin, admin.ModelAdmin):
    list_display = ['slug', 'content']
    save_on_top = False

@admin.register(Programme)
class ProgrammeAdmin(admin.ModelAdmin):
    pass

class InlineTopicAdmin(admin.TabularInline):
    model = Topic

class InlineSessionAdmin(admin.TabularInline):
    model = Session

@admin.register(Course)
class CourseAdmin(FunkySaveAdmin, admin.ModelAdmin):
    inlines = [InlineTopicAdmin, InlineSessionAdmin]
    list_display = ['order', '__str__', 'name', 'slug', 'url']
    list_display_links = ['__str__']
    list_filter = ['programmes']
    list_editable = ['order', 'name', 'slug']
    fields = ['name', 'slug', 'active', 'description', 'programmes']

class InlineAssignmentAdmin(admin.TabularInline):
    model = Assignment

class InlineDownloadAdmin(admin.StackedInline):
    model = Download
    extra = 1

class InlinePresentationAdmin(admin.StackedInline):
    model = Presentation
    extra = 1

class InlineClarificationAdmin(admin.StackedInline):
    model = Clarification
    extra = 1

@admin.register(Topic)
class TopicAdmin(FunkySaveAdmin, admin.ModelAdmin):
    def has_add_permission(self, request):
        return False
    list_filter = ['course']
    list_display = ['number', 'name', 'short_description']
    exclude = ['course', 'number']
    def short_description(self, topic):
        s = topic.description
        if len(s) > 250:
            s = s[:250] + '...'
        return s

@admin.register(Session)
class SessionAdmin(FunkySaveAdmin, admin.ModelAdmin):
    def has_add_permission(self, request):
        return False
    inlines = [InlineAssignmentAdmin, InlineDownloadAdmin, InlinePresentationAdmin]
    list_filter = ['course']
    list_display = ['number', '__str__', 'name', 'course', 'registration_enabled', 'active']
    list_display_links = ['__str__']
    list_editable = ['number', 'name', 'registration_enabled', 'active']
    exclude = ['course', 'number']

class InlineStepAdmin(admin.TabularInline):
    model = Step

@admin.register(Assignment)
class AssignmentAdmin(FunkySaveAdmin, admin.ModelAdmin):
    def has_add_permission(self, request):
        return False
    inlines = [InlineStepAdmin]
    list_display = ['number', '__str__', 'session', 'name', 'nr_of_steps', 'locked', 'active']
    list_display_links = ['__str__']
    list_filter = ['session__course', 'session']
    list_editable = ['number', 'name', 'locked', 'active']
    exclude = ['session', 'number']

@admin.register(Step)
class StepAdmin(FunkySaveAdmin, admin.ModelAdmin):
    def has_add_permission(self, request):
        return False
    inlines = [InlineClarificationAdmin]
    list_display = ['number', '__str__', 'description', 'answer_required', 'assignment']
    list_display_links = ['__str__']
    list_editable = ['number', 'answer_required']
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
    list_display = ['__str__', 'session']
    exclude = ['session']

@admin.register(Presentation)
class PresentationAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False
    list_filter = ['session']
    list_display = ['__str__', 'session', 'visibility']
    radio_fields = {'visibility': admin.HORIZONTAL}
    exclude = ['session']

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False
    list_filter = ['session__course', 'session']
    list_display = ['number', 'date', 'session', 'ticket', 'nr_of_students', 'teacher', 'dismissed']
    exclude = ['session']

@admin.register(Clarification)
class ClarificationAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False
    list_filter = ['step__assignment__session']
    list_display = ['__str__', 'step', 'description']
    exclude = ['step']
