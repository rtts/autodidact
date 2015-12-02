from django.db import models
from django.conf import settings

class Discipline(models.Model):
    name = models.CharField(max_length=10, choices=(
        ('PSY', 'Psychology'),
        ('SOC', 'Sociology'),
        ('PEW', 'Human Resource Studies'),
        ('OW', 'Organization Studies'),
        ('GMSI', 'Global Management of Social Issues'),
    ))

class Course(models.Model):
    name = models.CharField(max_length=255)
    discipline = models.ForeignKey(Discipline, related_name='courses')

class Module(models.Model):
    name = models.CharField(max_length=255)
    courses = models.ManyToManyField(Course, related_name='modules')

class Assignment(models.Model):
    title = models.CharField(max_length=255)
    description = RichTextField()
    image = models.ImageField(blank=True)
    datafile = models.FileField(blank=True)
 
class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)

class Completed(models.Model):
    module = models.ForeignKey(Module)
    student = models.ForeignKey(Student)
    date = models.DateTimeField(auto_now_add=True)
    
