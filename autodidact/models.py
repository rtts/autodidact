from __future__ import unicode_literals
import os
from datetime import timedelta
from django.utils import timezone
from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from pandocfield import PandocField
from numberedmodel.models import NumberedModel
from .utils import clean

TICKET_LENGTH = 4

class Page(models.Model):
    slug = models.SlugField(blank=True, unique=True, help_text='Leave this field blank for the homepage')
    title = models.CharField(max_length=255, blank=True)
    content = PandocField(blank=True)

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        if self.slug:
            return reverse('page', args=[self.slug])
        else:
            return reverse('homepage')

class PageFile(models.Model):
    page = models.ForeignKey(Page, related_name='files')
    file = models.FileField()

    def __str__(self):
        return os.path.basename(str(self.file))

    class Meta:
        ordering = ['file']

class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Programme(NumberedModel):
    DEGREES = [
        (10, 'Bachelor'),
        (20, 'Pre-master'),
        (30, 'Master'),
    ]
    order = models.PositiveIntegerField(blank=True)
    degree = models.PositiveIntegerField(choices=DEGREES)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, null=True)
    description = PandocField(blank=True)

    def __str__(self):
        return self.name

    def number_with_respect_to(self):
        return self.__class__.objects.filter(degree=self.degree)

    def has_active_courses(self):
        return self.courses.filter(active=True).exists()

    class Meta:
        ordering = ['order']

class Course(NumberedModel):
    order = models.PositiveIntegerField(blank=True)
    program = models.ForeignKey(Programme, related_name='courses')
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = PandocField(blank=True)
    active = models.BooleanField(default=False, help_text='Inactive courses are not visible to students')

    def __str__(self):
        return '%s (%s)' % (self.name, self.colloquial_name())

    def colloquial_name(self):
        return self.slug.replace('-', ' ').replace('mto', 'mto-').upper()

    def url(self):
        return '<a href="%(url)s">%(url)s</a>' % {'url': self.get_absolute_url()}
    url.allow_tags = True

    def get_absolute_url(self):
        return reverse('course', args=[self.slug])

    class Meta:
        ordering = ['order']

class Topic(NumberedModel):
    number = models.PositiveIntegerField(blank=True)
    course = models.ForeignKey(Course, related_name="topics")
    name = models.CharField(max_length=255, blank=True)
    description = PandocField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('topic', args=[self.course.slug, self.number])

    def number_with_respect_to(self):
        return self.course.topics.all()

    class Meta:
        ordering = ['number']

class Session(NumberedModel):
    number = models.PositiveIntegerField(blank=True)
    course = models.ForeignKey(Course, related_name="sessions")
    name = models.CharField(max_length=255, blank=True)
    description = PandocField(blank=True)
    registration_enabled = models.BooleanField(default=True, help_text='When enabled, class attendance will be registered')
    active = models.BooleanField(default=False, help_text='Inactive sessions are not visible to students')
    tags = models.ManyToManyField(Tag, related_name='sessions', blank=True)

    def __str__(self):
        return '%s: Session %i' % (self.course.colloquial_name(), self.number)

    def get_absolute_url(self):
        return reverse('session', args=[self.course.slug, self.number])

    def number_with_respect_to(self):
        return self.course.sessions.all()

    class Meta:
        ordering = ['number']

class Assignment(NumberedModel):
    number = models.PositiveIntegerField(blank=True)
    session = models.ForeignKey(Session, related_name='assignments', help_text='You can move assignments between sessions by using this dropdown menu')
    name = models.CharField(max_length=255, blank=True)
    active = models.BooleanField(default=False, help_text='Inactive assignments are not visible to students')
    locked = models.BooleanField(default=False, help_text='Locked assignments can only be made by students in class')

    def __str__(self):
        return 'Assignment {}'.format(self.number)

    def nr_of_steps(self):
        return self.steps.count()

    def get_absolute_url(self):
        return reverse('assignment', args=[self.session.course.slug, self.session.number, self.number])

    def number_with_respect_to(self):
        #raise ValueError(self)
        return self.session.assignments.all()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Ensure at least one step
        if not self.steps.first():
            Step(assignment=self).save()

    class Meta:
        ordering = ['number']

class Step(NumberedModel):
    number = models.PositiveIntegerField(blank=True)
    assignment = models.ForeignKey(Assignment, related_name='steps')
    description = PandocField(blank=True)
    answer_required = models.BooleanField(default=False, help_text='If enabled, this step will show students an input field where they can enter their answer. Add one or more right answers below to have students’ answers checked for correctness.')

    def __str__(self):
        return 'Step {}'.format(self.number)

    def get_absolute_url(self):
        if hasattr(self, 'fullscreen') and self.fullscreen == True:
            parameter = '&fullscreen'
        else:
            parameter = ''

        return reverse('assignment', args=[
            self.assignment.session.course.slug,
            self.assignment.session.number,
            self.assignment.number,
        ]) + '?step=' + str(self.number) + parameter

    def number_with_respect_to(self):
        return self.assignment.steps.all()

    class Meta:
        ordering = ['number']

class RightAnswer(models.Model):
    step = models.ForeignKey(Step, related_name='right_answers')
    value = models.CharField(max_length=255, help_text='This value can either be a case-insensitive string or a numeric value. For numeric values you can use the <a target="_blank" href="https://docs.moodle.org/23/en/GIFT_format">GIFT notation</a> of "answer:tolerance" or "low..high".')

    def __str__(self):
        return 'Right answer for {}'.format(self.step)

class WrongAnswer(models.Model):
    step = models.ForeignKey(Step, related_name='wrong_answers')
    value = models.CharField(max_length=255, help_text='Supplying one or more wrong answers will turn this into a multiple choice question.')

    def __str__(self):
        return 'Wrong answer for {}'.format(self.step)

class CompletedStep(models.Model):
    step = models.ForeignKey(Step, related_name='completed')
    whom = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='completed')
    date = models.DateTimeField(auto_now_add=True)
    answer = models.TextField(blank=True)
    passed = models.BooleanField(default=True)

    def __str__(self):
        return '%s has completed %s' % (self.whom.username, str(self.step))

    class Meta:
        verbose_name_plural = 'completed steps'

class Class(models.Model):
    session = models.ForeignKey(Session, related_name='classes')
    number = models.CharField(max_length=16)
    ticket = models.CharField(unique=True, max_length=16)
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='attends', blank=True)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='teaches', blank=True, null=True)
    dismissed = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Class %s of %s' % (self.number, str(self.session))

    def nr_of_students(self):
        return self.students.count()

    class Meta:
        verbose_name_plural = 'classes'

class Download(models.Model):
    session = models.ForeignKey(Session, related_name='downloads')
    file = models.FileField()

    def __str__(self):
        return os.path.basename(str(self.file))

    def url(self):
        return self.file.url

    class Meta:
        ordering = ['file']

class Presentation(models.Model):
    session = models.ForeignKey(Session, related_name='presentations')
    file = models.FileField()
    visibility = models.IntegerField(choices=(
        (0, 'Invisible'),
        (1, 'Only visible to teacher'),
        (2, 'Visible to students in class'),
        (3, 'Visible to everyone'),
    ), default=1)

    def __str__(self):
        return os.path.basename(str(self.file))

    def url(self):
        return self.file.url

    class Meta:
        ordering = ['file']

class Clarification(NumberedModel):
    number = models.PositiveIntegerField(blank=True)
    step = models.ForeignKey(Step, related_name='clarifications')
    description = PandocField(blank=True)
    image = models.ImageField(blank=True)

    def __str__(self):
        return 'Clarification for %s' % str(self.step)

    def number_with_respect_to(self):
        return self.step.clarifications.all()

    class Meta:
        ordering = ['number']

class StepFile(models.Model):
    step = models.ForeignKey(Step, related_name='files')
    file = models.FileField()

    def __str__(self):
        return os.path.basename(str(self.file))

    class Meta:
        ordering = ['file']
