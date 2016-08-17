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

class InlineTopicAdmin(admin.StackedInline):
    model = Topic
    extra = 0

class InlineSessionAdmin(admin.StackedInline):
    model = Session
    extra = 0

class InlineAssignmentAdmin(admin.StackedInline):
    model = Assignment
    extra = 0

class InlineDownloadAdmin(admin.StackedInline):
    model = Download
    extra = 0

class InlinePresentationAdmin(admin.StackedInline):
    model = Presentation
    extra = 0

class InlineClarificationAdmin(admin.StackedInline):
    model = Clarification
    extra = 0

@admin.register(Programme)
class ProgrammeAdmin(admin.ModelAdmin):
    pass

@admin.register(Page)
class PageAdmin(FunkySaveAdmin, admin.ModelAdmin):
    list_display = ['name', 'title']
    save_on_top = False
    def name(self, page):
        return page.slug if page.slug else 'homepage'

@admin.register(Course)
class CourseAdmin(FunkySaveAdmin, admin.ModelAdmin):
    inlines = [InlineTopicAdmin, InlineSessionAdmin]
    list_display = ['order', 'name', 'url']
    list_display_links = ['name']
    list_filter = ['programmes']

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
    ordering = ['course__order', 'number']
    list_filter = ['course']
    list_display = ['__str__', 'name', 'course', 'registration_enabled', 'active']
    list_display_links = ['__str__']
    inlines = [InlineAssignmentAdmin, InlineDownloadAdmin, InlinePresentationAdmin]
    exclude = ['course', 'number']

class InlineStepAdmin(admin.StackedInline):
    model = Step
    extra = 0

@admin.register(Assignment)
class AssignmentAdmin(FunkySaveAdmin, admin.ModelAdmin):
    def has_add_permission(self, request):
        return False
    ordering = ['session__course__order', 'session__number', 'number']
    list_display = ['number', 'name', 'session', 'nr_of_steps', 'locked', 'active']
    list_display_links = ['name']
    list_filter = ['session__course', 'session']
    inlines = [InlineStepAdmin]
    exclude = ['session', 'number']

@admin.register(Step)
class StepAdmin(FunkySaveAdmin, admin.ModelAdmin):
    def has_add_permission(self, request):
        return False
    ordering = ['assignment__session__course__order', 'assignment__session__number', 'assignment__number', 'number']
    list_display = ['__str__', 'assignment', 'description', 'answer_required']
    list_filter = ['assignment__session', 'assignment']
    inlines = [InlineClarificationAdmin]
    exclude = ['assignment']

@admin.register(CompletedStep)
class CompletedStepAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False
    list_display = ['date', 'step', 'whom', 'answer']
    list_display_links = ['step']
    list_filter = ['step__assignment__session__course', 'whom']
    ordering = ['-date']
    exclude = ['step', 'whom']

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False
    list_filter = ['session__course', 'session']
    list_display = ['date', 'number', 'session', 'ticket', 'nr_of_students', 'teacher', 'dismissed']
    list_display_links = ['number']
    ordering = ['-date']
    fields = ['number', 'ticket', 'dismissed']
