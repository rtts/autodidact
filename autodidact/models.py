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
    course = models.ManyToManyField(Course, related_name='assignments')

    def __str__(self):
        return self.description

class Session(models.Model):
    number = models.IntegerField()
    courses = models.ManyToManyField(Course, related_name='modules')

    def __str__(self):
        return 'Session ' + self.name

class Download(models.Model):
    description = models.CharField(max_length=255)
    file = models.FileField(blank=True)
    session = models.ManyToManyField(Session, related_name='downloads')

    def __str__(self):
        return self.description

class Question(PolymorphicModel):
    text = models.TextField()
    type = models.CharField(max_length=10, choices=(
        ('Bool', 'True/False'),
        ('Int', 'Integer'),
        ('Float', 'Floating-point number'),
        ('String', 'Text input'),
        ('Radio', 'Select the right answer'),
        ('Checkbox', 'Select multiple right answers'),
    ))
    def __str__(self):
        return self.description

class BoolQuestion(Question):
    correct_answer = models.BooleanField();

class IntQuestion(Question):
    correct_answer = models.IntegerField();

class FloatQuestion(Question):
    integer_part = models.IntegerField();
    fractional_part = models.IntegerField();
    precision = models.IntegerField();

class StringQuestion(Question):
    correct_answer = models.CharField(max_length=255);

class RadioQuestion(Question):
    pass

class CheckboxQuestion(Question):
    pass

class MultipleChoiceAnswer(models.Model):
    text = models.CharField(max_length=255)
    correct = models.BooleanField()
    question = models.ForeignKey(Question)

class Activity(PolymorphicModel):
    title = models.CharField(max_length=255)
    session = models.ManyToManyField(Session, related_name='activities')

    def __str__(self):
        return self.title

class ReadingActivity(Activity):
    wall_of_text = models.TextField()

class QuestionActivity(Activity):
    question = models.ForeignKey(Question)

class CompletedActivity(models.Model):
    activity = models.ForeignKey(Activity)
    whom = models.ForeignKey(settings.AUTH_USER_MODEL)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s has completed %s' % (self.student.user.username, self.module.name)
