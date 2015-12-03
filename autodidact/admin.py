from django.contrib import admin
from django.db import models
from django.forms import RadioSelect
from .models import *
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin

@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    pass

class InlineSessionAdmin(admin.TabularInline):
    model = Session

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [InlineSessionAdmin]

class BooleanQuestionAdmin(PolymorphicChildModelAdmin):
    base_model = Question

class IntegerQuestionAdmin(PolymorphicChildModelAdmin):
    base_model = Question

class DecimalQuestionAdmin(PolymorphicChildModelAdmin):
    base_model = Question

class StringQuestionAdmin(PolymorphicChildModelAdmin):
    base_model = Question

class InlineMultipleChoiceAnswerAdmin(admin.TabularInline):
    model = MultipleChoiceAnswer
    extra = 2

class MultipleChoiceQuestionAdmin(PolymorphicChildModelAdmin):
    base_model = Question
    inlines = [InlineMultipleChoiceAnswerAdmin]

@admin.register(Question)
class QuestionAdmin(PolymorphicParentModelAdmin):
    base_model = Question
    child_models = (
        (BooleanQuestion, BooleanQuestionAdmin),
        (IntegerQuestion, IntegerQuestionAdmin),
        (DecimalQuestion, DecimalQuestionAdmin),
        (StringQuestion, StringQuestionAdmin),
        (MultipleChoiceQuestion, MultipleChoiceQuestionAdmin),
    )

class InstructionsAdmin(PolymorphicChildModelAdmin):
    base_model = Activity

class AssessmentAdmin(PolymorphicChildModelAdmin):
    base_model = Activity

@admin.register(Activity)
class ActivityAdmin(PolymorphicParentModelAdmin):
    base_model = Activity
    child_models = (
        (Instructions, InstructionsAdmin),
        (Assessment, AssessmentAdmin),
    )
    list_filter = ['session']

