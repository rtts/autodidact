from django.db import models
from django.conf import settings
from polymorphic import PolymorphicModel

class Discipline(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=255)
    discipline = models.ForeignKey(Discipline, related_name='courses')

    def __str__(self):
        return self.name

class Assignment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    result = models.FileField(blank=True)
    course = models.ForeignKey(Course)

    def __str__(self):
        return self.description

class Session(models.Model):
    name = models.CharField(max_length=255)
    course = models.ForeignKey(Course)

    def __str__(self):
        return '%s - %s' % (self.course, self.name)

class Download(models.Model):
    description = models.CharField(max_length=255)
    file = models.FileField(blank=True)
    session = models.ManyToManyField(Session, related_name='downloads')

    def __str__(self):
        return self.description

class Question(PolymorphicModel):
    text = models.TextField()
    reusable = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class BooleanQuestion(Question):
    correct_answer = models.BooleanField(default=True, choices=(
        (True, 'True'),
        (False, 'False'),
    ))

class IntegerQuestion(Question):
    correct_answer = models.IntegerField()

class DecimalQuestion(Question):
    integer_part = models.IntegerField()
    fractional_part = models.IntegerField()
    precision = models.IntegerField()

class StringQuestion(Question):
    correct_answer = models.CharField(max_length=255)
    case_sensitive = models.BooleanField(default=False)

class MultipleChoiceQuestion(Question):
    pass

class MultipleChoiceAnswer(models.Model):
    answer = models.CharField(max_length=255)
    correct = models.BooleanField()
    question = models.ForeignKey(Question)

class Activity(PolymorphicModel):
    title = models.CharField(max_length=255)
    session = models.ForeignKey(Session, related_name='activities')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'activities'

class Instructions(Activity):
    wall_of_text = models.TextField()

class Assessment(Activity):
    description = models.TextField()
    questions = models.ManyToManyField(Question)

class CompletedActivity(models.Model):
    activity = models.ForeignKey(Activity)
    whom = models.ForeignKey(settings.AUTH_USER_MODEL)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s has completed %s' % (self.student.user.username, self.module.name)
