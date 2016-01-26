from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from adminsortable.models import SortableMixin
from adminsortable.fields import SortableForeignKey

class Programme(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Course(SortableMixin):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    programmes = models.ManyToManyField(Programme, related_name='courses')
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    def colloquial_name(self):
        return self.slug.replace('-', ' ').replace('mto', 'mto-').upper()

    def __str__(self):
        return '%s (%s)' % (self.name, self.colloquial_name())

    def get_absolute_url(self):
        return reverse('course', args=[self.slug])

    class Meta:
        ordering = ['order']

class Session(SortableMixin):
    name = models.CharField(max_length=255)
    description = models.TextField()
    course = SortableForeignKey(Course, related_name="sessions")
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    def __str__(self):
        return '%s: Session %i' % (self.course.colloquial_name(), self.get_number())

    def get_number(self):
        return self.course.sessions.filter(order__lt=self.order).count() + 1

    def get_absolute_url(self):
        return reverse('session', args=[self.course.slug, self.get_number()])

    class Meta:
        ordering = ['order']

class Assignment(SortableMixin):
    name = models.CharField(max_length=255)
    session = SortableForeignKey(Session, related_name="assignments")
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    def __str__(self):
        return '%s: %s' % (self.session.name, self.name)

    def get_number(self):
        return self.session.assignments.filter(order__lt=self.order).count() + 1

    def get_absolute_url(self):
        return reverse('assignment', args=[self.session.course.slug, self.session.get_number(), self.get_number()])

    class Meta:
        ordering = ['order']

class Activity(SortableMixin):
    name = models.CharField(max_length=255)
    assignment = SortableForeignKey(Assignment, related_name='activities')
    description = models.TextField()
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)
    answer_required = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_number(self):
        return self.assignments.activities.filter(order__lt=self.order).count() + 1

    class Meta:
        verbose_name_plural = 'activities'
        ordering = ['order']

class CompletedActivity(models.Model):
    activity = models.ForeignKey(Activity, related_name='completed')
    whom = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='completed')
    date = models.DateTimeField(auto_now_add=True)
    answer = models.TextField(blank=True)

    def __str__(self):
        return '%s has completed %s' % (self.whom.username, self.activity.name)

    class Meta:
        verbose_name_plural = 'completed activities'

class Download(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(blank=True)
    session = models.ManyToManyField(Session, related_name='downloads')

    def __str__(self):
        return self.name

