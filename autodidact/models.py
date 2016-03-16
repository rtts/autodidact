from __future__ import unicode_literals
import os
from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.encoding import python_2_unicode_compatible
from adminsortable.models import SortableMixin
from adminsortable.fields import SortableForeignKey
from .utils import clean

MDHELP = 'This field supports <a target="_blank" href="http://daringfireball.net/projects/markdown/syntax">Markdown syntax</a>'
TICKET_LENGTH = 4

@python_2_unicode_compatible
class Page(models.Model):
    slug = models.SlugField(blank=True, unique=True)
    content = models.TextField(help_text=MDHELP)

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        if self.slug:
            return reverse('page', args=[self.slug])
        else:
            return reverse('homepage')

@python_2_unicode_compatible
class Programme(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Course(SortableMixin):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(help_text=MDHELP)
    programmes = models.ManyToManyField(Programme, related_name='courses')
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)
    active = models.BooleanField(default=True, help_text='Inactive courses are not visible to students')

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

@python_2_unicode_compatible
class Session(SortableMixin):
    name = models.CharField(max_length=255, blank=True)
    description = models.TextField(help_text=MDHELP, blank=True)
    course = SortableForeignKey(Course, related_name="sessions")
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)
    registration_enabled = models.BooleanField(default=True, help_text='When enabled, class attendance will be registered')
    active = models.BooleanField(default=True, help_text='Inactive sessions are not visible to students')

    def __str__(self):
        return '%s: Session %i' % (self.course.colloquial_name(), self.get_number())

    def get_number(self):
        return self.course.sessions.filter(order__lt=self.order).count() + 1

    def get_absolute_url(self):
        return reverse('session', args=[self.course.slug, self.get_number()])

    class Meta:
        ordering = ['order']

@python_2_unicode_compatible
class Assignment(SortableMixin):
    name = models.CharField(max_length=255, blank=True)
    session = SortableForeignKey(Session, related_name="assignments")
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)
    active = models.BooleanField(default=False, help_text='Inactive assignments are not visible to students')
    locked = models.BooleanField(default=True, help_text='Locked assignments can only be made by students in class')

    def __str__(self):
        return 'Assignment {}'.format(self.get_number())

    def get_number(self):
        return self.session.assignments.filter(order__lt=self.order).count() + 1

    def nr_of_steps(self):
        return self.steps.count()

    def get_absolute_url(self):
        return reverse('assignment', args=[self.session.course.slug, self.session.get_number(), self.get_number()])

    class Meta:
        ordering = ['order']

    # Override the save method to ensure at least one step
    def save(self, *args, **kwargs):
        super(Assignment, self).save(*args, **kwargs)
        if not self.steps.first():
            Step(assignment=self).save()

@python_2_unicode_compatible
class Step(SortableMixin):
    name = models.CharField(max_length=255, blank=True)
    assignment = SortableForeignKey(Assignment, related_name='steps')
    description = models.TextField(help_text=MDHELP, blank=True)
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)
    answer_required = models.BooleanField(default=False, help_text='If enabled, this step will show the student a text box where they can enter their answer')

    def __str__(self):
        return 'Step {}'.format(self.get_number())

    def get_number(self):
        return self.assignment.steps.filter(order__lt=self.order).count() + 1

    def get_absolute_url(self):
        return reverse('assignment', args=[
            self.assignment.session.course.slug,
            self.assignment.session.get_number(),
            self.assignment.get_number(),
        ]) + '?step=' + str(self.get_number())

    class Meta:
        ordering = ['order']

@python_2_unicode_compatible
class CompletedStep(models.Model):
    step = models.ForeignKey(Step, related_name='completed')
    whom = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='completed')
    date = models.DateTimeField(auto_now_add=True)
    answer = models.TextField(blank=True)

    def __str__(self):
        return '%s has completed %s' % (self.whom.username, str(self.step))

    class Meta:
        verbose_name_plural = 'completed steps'

@python_2_unicode_compatible
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

def session_path(obj, filename):
    return os.path.join(obj.session.get_absolute_url()[1:], clean(filename))

@python_2_unicode_compatible
class Download(models.Model):
    file = models.FileField(upload_to=session_path)
    session = models.ForeignKey(Session, related_name='downloads')

    def __str__(self):
        return os.path.basename(str(self.file))

    def url(self):
        return self.file.url

    def filename(self):
        return os.basename(self.file)

    class Meta:
        ordering = ['file']

@python_2_unicode_compatible
class Presentation(SortableMixin):
    file = models.FileField(upload_to=session_path)
    session = SortableForeignKey(Session, related_name='presentations')
    visibility = models.IntegerField(choices=(
        (1, 'Only visible to teacher'),
        (2, 'Visible to students in class'),
        (3, 'Visible to everyone'),
    ))
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    def __str__(self):
        return os.path.basename(str(self.file))

    def url(self):
        return self.file.url

    class Meta:
        ordering = ['order']

def image_path(obj, filename):
    return os.path.join(obj.step.assignment.session.get_absolute_url()[1:], 'images', clean(filename))

@python_2_unicode_compatible
class Clarification(SortableMixin):
    step = models.ForeignKey(Step, related_name='clarifications')
    description = models.TextField(help_text=MDHELP)
    image = models.ImageField(upload_to=image_path)
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    def __str__(self):
        return 'Clarification for %s' % unicode(self.step)

    class Meta:
        ordering = ['order']
