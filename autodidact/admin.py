from django.contrib import admin
from django.db import models
from django.forms import RadioSelect
from django.shortcuts import redirect
from django.utils.safestring import mark_safe
from django.forms import CheckboxSelectMultiple
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
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

@admin.register(Topic)
class TopicAdmin(FunkySaveAdmin, admin.ModelAdmin):
    save_on_top = False
    list_filter = ['course']
    list_display = ['number', 'name', 'short_description']
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
    inlines = [InlineAssignmentAdmin, InlineDownloadAdmin, InlinePresentationAdmin]
    exclude = ['course']

class InlineStepAdmin(admin.StackedInline):
    model = Step
    extra = 0

@admin.register(Assignment)
class AssignmentAdmin(FunkySaveAdmin, admin.ModelAdmin):
    ordering = ['session__course__order', 'session__number', 'number']
    list_display = ['number', 'name', 'session', 'nr_of_steps', 'active', 'locked']
    list_display_links = ['name']
    list_filter = ['active', 'locked', 'session__course', 'session']
    inlines = [InlineStepAdmin]

@admin.register(Step)
class StepAdmin(FunkySaveAdmin, admin.ModelAdmin):
    def has_add_permission(self, request):
        return False
    ordering = ['assignment__session__course__order', 'assignment__session__number', 'assignment__number', 'number']
    list_display = ['__str__', 'assignment', 'get_description', 'answer_required']
    list_filter = ['assignment__session', 'assignment']
    inlines = [InlineClarificationAdmin]
    exclude = ['assignment']

    def get_description(self, obj):
        return mark_safe(obj.description.raw.replace('\n', '<br>'))

@admin.register(CompletedStep)
class CompletedStepAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False
    list_display = ['date', 'step', 'whom', 'answer']
    list_display_links = ['step']
    list_filter = ['step__assignment__session__course', 'whom']
    ordering = ['-date']
    exclude = ['step', 'whom']

class InlineQuestionAdmin(admin.StackedInline):
    model = Question
    extra = 0
    fields = ['number', 'description', 'edit_link']
    readonly_fields = ['edit_link']

    def edit_link(self, instance):
        url = reverse('admin:{}_{}_change'.format(instance._meta.app_label, instance._meta.model_name), args=[instance.pk])
        if instance.pk:
            return mark_safe('<a href="{}">Edit</a><p class="help">This link will take you to the question editor. If you have made any changes on this page, please make sure to hit the "save" button first!</p>'.format(url))
        else:
            return '(please save this question first)'
    edit_link.short_description = 'Possible answers'

class InlineQuizFileAdmin(admin.StackedInline):
    model = QuizFile
    extra = 0

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    ordering = ['course__order', 'number']
    list_display = ['__str__', 'course', 'nr_of_questions']
    list_filter = ['course']
    exclude = ['number']
    inlines = [InlineQuizFileAdmin, InlineQuestionAdmin]

@admin.register(CompletedQuiz)
class CompletedQuizAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False
    list_display = ['date', 'quiz', 'whom']
    list_display_links = ['quiz']
    list_filter = ['quiz__course', 'whom']
    ordering = ['-date']
    exclude = ['quiz', 'whom']

class InlineRightAnswerAdmin(admin.StackedInline):
    model = RightAnswer
    extra = 1

class InlineWrongAnswerAdmin(admin.StackedInline):
    model = WrongAnswer
    extra = 0

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    def response_change(self, request, obj):
        if '_save' in request.POST:
            return redirect('admin:autodidact_quiz_change', obj.quiz.pk)
        else:
            return super(QuestionAdmin, self).response_change(request, obj)

    # Hide this admin from the admin index
    def get_model_perms(self, request):
        return {}

    def has_add_permission(self, request):
        return False

    ordering = ['quiz__course__order', 'number']
    list_display = ['__str__', 'quiz', 'description']
    list_filter = ['quiz__course', 'quiz']
    exclude = ['quiz']
    inlines = [InlineRightAnswerAdmin, InlineWrongAnswerAdmin]

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False
    list_filter = ['session__course', 'session']
    list_display = ['date', 'number', 'session', 'ticket', 'nr_of_students', 'teacher', 'dismissed']
    list_display_links = ['number']
    ordering = ['-date']
    fields = ['number', 'ticket', 'dismissed']
