from django.db import models
from django.conf import settings
from adminsortable.models import SortableMixin
from adminsortable.fields import SortableForeignKey

class Discipline(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Course(SortableMixin):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    discipline = models.ForeignKey(Discipline, related_name='courses')
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']

class Session(SortableMixin):
    name = models.CharField(max_length=255)
    course = SortableForeignKey(Course)
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    def __str__(self):
        return '%s - %s' % (self.course, self.name)

    class Meta:
        ordering = ['order']

class Download(models.Model):
    description = models.CharField(max_length=255)
    file = models.FileField(blank=True)
    session = models.ManyToManyField(Session, related_name='downloads')

    def __str__(self):
        return self.description

class Activity(SortableMixin):
    title = models.CharField(max_length=255)
    session = SortableForeignKey(Session, related_name='activities')
    wall_of_text = models.TextField()
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'activities'
        ordering = ['order']

class CompletedActivity(models.Model):
    activity = models.ForeignKey(Activity)
    whom = models.ForeignKey(settings.AUTH_USER_MODEL)
    date = models.DateTimeField(auto_now_add=True)
    answer = models.TextField(blank=True)

    def __str__(self):
        return '%s has completed %s' % (self.student.user.username, self.module.name)

    class Meta:
        verbose_name_plural = 'completed activities'
