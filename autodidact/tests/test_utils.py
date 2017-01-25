# coding: utf-8
from __future__ import unicode_literals

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from ..utils import *
from ..models import *

unicode_string = '☀☁☂☃☄★☆☇☈'
course_name = 'Test Course ☆'
course_slug = 'mtoc-psy'
password = unicode_string

class UtilsTest(TestCase):
    def setUp(self):
        self.teacher = get_user_model()(username='teacher', is_staff=True)
        self.teacher.set_password(password)
        self.teacher.save()
        self.student = get_user_model()(username='student')
        self.student.set_password(password)
        self.student.save()
        self.course = Course(name=course_name, slug=course_slug)
        self.course.save()
        self.session = Session(course=self.course)
        self.session.save()
        self.assignment1 = Assignment(session=self.session)
        self.assignment1.save()
        self.assignment = self.assignment1
        self.assignment2 = Assignment(session=self.session)
        self.assignment2.save()
        self.assignment3 = Assignment(session=self.session)
        self.assignment3.save()
        self.klass = Class(session=self.session, ticket='123')
        self.klass.save()

    def test_get_current_class(self):
        '''For teachers, the current class is first class in a session they are teaching. For students, the current class is the first class in a session they are attending.'''
        self.assertIsNone(get_current_class(self.session, self.student))
        self.assertIsNone(get_current_class(self.session, self.teacher))
        self.klass.teacher = self.teacher
        self.klass.students.add(self.student)
        self.klass.save()
        self.assertEqual(get_current_class(self.session, self.student), self.klass)
        self.assertEqual(get_current_class(self.session, self.teacher), self.klass)

    def test_calculate_progress(self):
        '''Given a user and a list of assignments, calculate_progress() returns a list of percentages.'''

        Step(assignment=self.assignment1).save()
        Step(assignment=self.assignment1).save()
        Step(assignment=self.assignment1).save()
        # Assignment 1 now has 4 steps (1 initial + 3 added)

        CompletedStep(step=self.assignment1.steps.all()[0], whom=self.student).save()
        CompletedStep(step=self.assignment1.steps.all()[1], whom=self.student).save()
        CompletedStep(step=self.assignment1.steps.all()[2], whom=self.student).save()
        # 3 of 4 steps are now completed, i.e. 75%

        progress = calculate_progress(self.student, [self.assignment1])
        self.assertEqual(len(progress), 0)

        self.assignment1.active = True
        self.assignment1.save()

        progress = calculate_progress(self.student, [self.assignment1])
        self.assertEqual(len(progress), 1)
        self.assertEqual(progress[0], 75)
        self.assertTrue(isinstance(progress[0], int))

        self.assignment2.active = True
        self.assignment2.save()
        self.assignment3.active = True
        self.assignment3.save()

        progress = calculate_progress(self.student, Assignment.objects.all())
        self.assertEqual(len(progress), 3)

    def test_clean(self):
        '''Cleans dirty filenames'''

        self.assertEqual(clean('&& `rm -rf /`'), ' rm -rf ')
        self.assertEqual(clean('/etc/passwd'), 'etcpasswd')
        self.assertEqual(clean('☀☁☂☃☄★☆☇☈'), '')
        self.assertEqual(clean('☀ēïçūô'), 'eicuo')
        self.assertEqual(clean('Valid Filename.pdf'), 'Valid Filename.pdf')
        self.assertEqual(clean(''), '')
