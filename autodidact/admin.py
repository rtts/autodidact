from django.contrib import admin
from django.db import models
from django.forms import RadioSelect
from django.shortcuts import redirect
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.forms import CheckboxSelectMultiple
from django.contrib.contenttypes.admin import GenericStackedInline
from .utils import duplicate_assignment, duplicate_session, duplicate_course
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

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_return'] = True
        return super().change_view(
            request, form_url, extra_context=extra_context,
        )

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_return'] = True
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )

class InlinePageFileAdmin(admin.StackedInline):
    model = PageFile
    extra = 0

class InlineStepFileAdmin(admin.StackedInline):
    model = StepFile
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

class InlineRightAnswerAdmin(admin.StackedInline):
    model = RightAnswer
    extra = 0

class InlineWrongAnswerAdmin(admin.StackedInline):
    model = WrongAnswer
    extra = 0

class InlineClarificationAdmin(admin.StackedInline):
    model = Clarification
    extra = 0

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass

@admin.register(Program)
class ProgramAdmin(FunkySaveAdmin, admin.ModelAdmin):
    list_display = ['name', 'slug', 'degree']
    list_display_links = ['name']
    ordering = ['degree', 'order']
    prepopulated_fields = {'slug': ['name']}

@admin.register(Page)
class PageAdmin(FunkySaveAdmin, admin.ModelAdmin):
    list_display = ['title', 'slug']
    save_on_top = False
    inlines = [InlinePageFileAdmin]

@admin.register(Course)
class CourseAdmin(FunkySaveAdmin, admin.ModelAdmin):
    list_display = ['__str__', 'order', 'url']
    list_filter = ['programs']
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }
    actions = [duplicate_course]

@admin.register(Topic)
class TopicAdmin(FunkySaveAdmin, admin.ModelAdmin):
    save_on_top = False
    list_filter = ['course']
    exclude = ['course', 'number']

    def has_add_permission(self, request):
        return False

    def short_description(self, topic):
        s = topic.description.raw
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
    inlines = [InlineDownloadAdmin, InlinePresentationAdmin]
    exclude = ['course']
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }
    actions = [duplicate_session]

@admin.register(Assignment)
class AssignmentAdmin(FunkySaveAdmin, admin.ModelAdmin):
    ordering = ['session__course__order', 'session__number', 'number']
    list_display = ['__str__', 'session', 'nr_of_steps', 'active', 'locked']
    list_filter = ['active', 'locked', 'session__course', 'session']
    actions = [duplicate_assignment]

@admin.register(Step)
class StepAdmin(FunkySaveAdmin, admin.ModelAdmin):
    def has_add_permission(self, request):
        return False
    ordering = ['assignment__session__course__order', 'assignment__session__number', 'assignment__number', 'number']
    list_display = ['__str__', 'assignment', 'get_description', 'answer_required']
    list_filter = ['assignment__session', 'assignment']
    inlines = [InlineRightAnswerAdmin, InlineWrongAnswerAdmin, InlineClarificationAdmin, InlineStepFileAdmin]
    exclude = ['assignment']
    save_on_top = True

    def get_description(self, obj):
        return mark_safe(obj.description.raw.replace('\n', '<br>'))

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False
    list_filter = ['session__course', 'session']
    list_display = ['date', 'number', 'session', 'ticket', 'nr_of_students', 'teacher', 'dismissed']
    list_display_links = ['number']
    ordering = ['-date']
    fields = ['number', 'ticket', 'dismissed']
