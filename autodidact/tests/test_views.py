# coding: utf-8
from __future__ import unicode_literals

import os, sys
import datetime
import shutil
from django.conf import settings
from django.test import TestCase, Client
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from ..models import *

unicode_string = '☀☁☂☃☄★☆☇☈'
course_name = 'Test Course ☆'
course_slug = 'mtoc-psy'
username = 'testuser'
password = unicode_string

class PageViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model()(username=username)
        self.user.set_password(password)
        self.user.save()
        self.page = Page(slug='test', content=unicode_string)
        self.page.save()
        self.programme = Programme(name=unicode_string)
        self.programme.save()

    def test_context_variables(self):
        '''The page() view supplies the context variables "page" and "programmes"'''

        c = Client()
        c.login(username=username, password=password)
        url = reverse('homepage')
        response = c.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['programmes'], map(repr, Programme.objects.all()))

class CourseViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model()(username=username)
        self.user.set_password(password)
        self.user.save()
        self.course = Course(name=course_name, slug=course_slug, active=True)
        self.course.save()

    def test_context_variables(self):
        '''The course() view supplies the context variable "course"'''

        c = Client()
        c.login(username=username, password=password)
        url = reverse('course', args=[course_slug])
        response = c.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['course'], self.course)

class SessionViewTest(TestCase):
    valid_ticket = 'a123'
    invalid_ticket = 'b456'
    def setUp(self):
        self.user = get_user_model()(username=username)
        self.user.set_password(password)
        self.user.save()
        self.course = Course(name=course_name, slug=course_slug, active=True)
        self.course.save()
        self.session = Session(course=self.course, active=True)
        self.session.save()
        self.assignment1 = Assignment(session=self.session)
        self.assignment1.save()
        self.assignment = self.assignment1
        self.assignment2 = Assignment(session=self.session)
        self.assignment2.save()
        self.assignment3 = Assignment(session=self.session)
        self.assignment3.save()
        self.klass = Class(session=self.session, ticket=self.valid_ticket)
        self.klass.save()

    def test_context_variables(self):
        '''The session() view supplies the context variables "course", "session", and "assignments"'''

        c = Client()
        c.login(username=username, password=password)
        url = reverse('session', args=[course_slug, '1'])
        response = c.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['course'], self.course)
        self.assertEqual(response.context['session'], self.session)
        self.assertQuerysetEqual(response.context['assignments'], map(repr, self.session.assignments.all()))

    def test_post_ticket(self):
        '''A successful POST to the session() view returns a 302 redirect'''

        c = Client()
        c.login(username=username, password=password)
        url = reverse('session', args=[course_slug, '1'])
        response = c.post(url, {'ticket': self.invalid_ticket})
        self.assertEqual(response.context['ticket_error'], self.invalid_ticket)
        response = c.post(url, {'ticket': self.valid_ticket})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.endswith(url))

    def test_students_and_teacher(self):
        '''When the requester is a staff user, the session() view supplies the context variable "students"'''

        student1 = get_user_model()(username='student1')
        student1.set_password(password)
        student1.save()
        student2 = get_user_model()(username='student2')
        student2.set_password(password)
        student2.save()
        student3 = get_user_model()(username='student3')
        student3.set_password(password)
        student3.save()
        teacher = self.user
        teacher.is_staff = True
        teacher.save()
        self.klass.teacher = teacher
        self.klass.students.add(student1, student2, student3)
        self.klass.save()

        c = Client()
        c.login(username=username, password=password)
        url = reverse('session', args=[course_slug, '1'])
        response = c.get(url)
        self.assertQuerysetEqual(response.context['students'], map(repr, self.klass.students.all()), ordered=False)

class ProgressViewTest(TestCase):
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

    def test_context_variables(self):
        '''The progress() view supplies the context variables "course", "session", "student", and "assignments"'''
        c = Client()
        c.login(username='teacher', password=password)
        url = reverse('progress', args=[course_slug, '1', 'invalid_username'])
        response = c.get(url)
        self.assertEqual(response.status_code, 404)
        url = reverse('progress', args=[course_slug, '1', 'student'])
        response = c.get(url)
        self.assertEqual(response.context['course'], self.course)
        self.assertEqual(response.context['session'], self.session)
        self.assertEqual(response.context['student'], self.student)
        self.assertQuerysetEqual(response.context['assignments'], map(repr, self.session.assignments.all()))

class ProgressesViewTest(TestCase):
    def setUp(self):
        self.teacher = get_user_model()(username='teacher', is_staff=True)
        self.teacher.set_password(password)
        self.teacher.save()
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
        self.student1 = get_user_model()(username='student1')
        self.student1.set_password(password)
        self.student1.save()
        self.student2 = get_user_model()(username='student2')
        self.student2.set_password(password)
        self.student2.save()
        self.student3 = get_user_model()(username='student3')
        self.student3.set_password(password)
        self.student3.save()
        self.klass = Class(session=self.session, ticket='123', teacher=self.teacher)
        self.klass.save()
        self.klass.students.add(self.student1, self.student2, self.student3)
        self.klass.save()

    def test_get_parameter(self):
        '''The GET parameter "days" must be present and valid'''

        c = Client()
        c.login(username='teacher', password=password)
        url = reverse('progresses', args=[course_slug, '1'])
        response = c.get(url)
        self.assertEqual(response.status_code, 400)
        response = c.get(url, {'days': 'haha'})
        self.assertEqual(response.status_code, 400)
        response = c.get(url, {'days': -1})
        self.assertEqual(response.status_code, 400)
        response = c.get(url, {'days': 365001})
        self.assertEqual(response.status_code, 400)
        response = c.get(url, {'days': 1})
        self.assertEqual(response.status_code, 200)

    def test_context_variables(self):
        '''The progresses() view supplies the context variables "course", "session", "current_class", "assignments", and "students".'''

        c = Client()
        c.login(username='teacher', password=password)
        url = reverse('progresses', args=[course_slug, '1'])
        response = c.get(url, {'days': 1})
        self.assertEqual(response.context['course'], self.course)
        self.assertEqual(response.context['session'], self.session)
        self.assertEqual(response.context['current_class'], self.klass)
        self.assertQuerysetEqual(response.context['students'], map(repr, self.klass.students.all()), ordered=False)
        self.assertQuerysetEqual(response.context['assignments'], map(repr, self.session.assignments.all()))

class AssignmentViewTest(TestCase):
    def setUp(self):
        self.teacher = get_user_model()(username='teacher', is_staff=True)
        self.teacher.set_password(password)
        self.teacher.save()
        self.course = Course(name=course_name, slug=course_slug, active=True)
        self.course.save()
        self.session = Session(course=self.course, active=True)
        self.session.save()
        self.assignment = Assignment(session=self.session, active=True)
        self.assignment.save()
        self.step1 = self.assignment.steps.first()
        self.step2 = Step(assignment=self.assignment)
        self.step2.save()
        self.step3 = Step(assignment=self.assignment)
        self.step3.save()
        self.student = get_user_model()(username='student')
        self.student.set_password(password)
        self.student.save()
        self.klass = Class(session=self.session, ticket='123', teacher=self.teacher)
        self.klass.save()
        self.klass.students.add(self.student)
        self.klass.save()

    def test_context_variables(self):
        '''The assignment() view supplies the context variables "course", "session", "assignment", "step", "first", "last", and "count"'''

        c = Client()
        c.login(username='student', password=password)
        url = reverse('assignment', args=[course_slug, '1', '1']) + '?step=1'
        self.assignment.active = True
        self.assignment.save()
        response = c.get(url)
        self.assertEqual(response.context['course'], self.course)
        self.assertEqual(response.context['session'], self.session)
        self.assertEqual(response.context['assignment'], self.assignment)
        self.assertEqual(response.context['step'], self.step1)

    def test_post_answer(self):
        '''When an answer is submitted in a POST request, a CompletedStep object is created or updated'''

        answer1 = '𝑝 ≥ 0.05'
        answer2 = '𝑝 < 0.05'
        c = Client()
        c.login(username='student', password=password)
        url = reverse('assignment', args=[course_slug, '1', '1']) + '?step=1'
        self.assignment.active = True
        self.assignment.save()
        response = c.post(url, {'answer': answer1})
        self.assertEqual(response.status_code, 302)
        response = c.get(url)
        self.assertEqual(response.context['step'].completedstep.answer, answer1)
        response = c.post(url, {'answer': answer2})
        self.assertEqual(response.status_code, 302)
        response = c.get(url)
        self.assertEqual(response.context['step'].completedstep.answer, answer2)

class StartclassViewTest(TestCase):
    def setUp(self):
        self.teacher = get_user_model()(username='teacher', is_staff=True)
        self.teacher.set_password(password)
        self.teacher.save()
        self.course = Course(name=course_name, slug=course_slug)
        self.course.save()
        self.session = Session(course=self.course)
        self.session.save()

    def test_create_class_and_redirect(self):
        '''A successful POST to the startclass() view creates a new class and redirects to the session page'''
        c = Client()
        c.login(username='teacher', password=password)
        url = reverse('startclass')
        self.assertEqual(c.get(url).status_code, 405)
        self.assertEqual(c.post(url, {'class_nr': 'testclassnumbertoolong'}).status_code, 400)
        self.assertEqual(c.post(url, {'class_nr': 'testclass'}).status_code, 404)
        self.assertEqual(c.post(url, {'session': '348734', 'class_nr': 'testclass'}).status_code, 404)
        self.assertRedirects(c.post(url, {'session': '1', 'class_nr': 'testclass'}), reverse('session', args=[self.course.slug, 1]))
        self.assertTrue(Class.objects.exists())
        self.assertEqual(Class.objects.first().teacher, self.teacher)

class EndclassViewTest(TestCase):
    def setUp(self):
        self.teacher = get_user_model()(username='teacher', is_staff=True)
        self.teacher.set_password(password)
        self.teacher.save()
        self.course = Course(name=course_name, slug=course_slug)
        self.course.save()
        self.session = Session(course=self.course)
        self.session.save()
        self.klass = Class(session=self.session, ticket='123', teacher=self.teacher)
        self.klass.save()

    def test_create_class_and_redirect(self):
        '''A successful POST to the endclass() view dismisses class and redirects to the session page'''
        c = Client()
        c.login(username='teacher', password=password)
        url = reverse('endclass')
        self.assertEqual(c.get(url).status_code, 405)
        self.assertEqual(c.post(url, {'session': '12314'}).status_code, 404)
        self.assertRedirects(c.post(url, {'session': '1'}), reverse('session', args=[self.course.slug, 1]))
        self.assertRedirects(c.post(url, {'session': '1', 'class': '1'}), reverse('session', args=[self.course.slug, 1]))
        self.assertTrue(Class.objects.first().dismissed)

        # The teacher remains after the class is dismissed, for future reference
        self.assertTrue(Class.objects.first().teacher)

class AddAssignmentTest(TestCase):
    def setUp(self):
        self.teacher = get_user_model()(username='teacher', is_staff=True, is_superuser=True)
        self.teacher.set_password(password)
        self.teacher.save()
        self.course = Course(name=course_name, slug=course_slug)
        self.course.save()
        self.session = Session(course=self.course)
        self.session.save()

    def test_add_assignment(self):
        '''The add_assignment() view creates a new assignment and redirect to the admin'''
        c = Client()
        c.login(username='teacher', password=password)
        self.assertFalse(Assignment.objects.exists())
        url = reverse('add_assignment', args=[self.course.slug, 1])
        c.get(url)
        self.assertTrue(self.session.assignments.exists())

class AddStepTest(TestCase):
    def setUp(self):
        self.teacher = get_user_model()(username='teacher', is_staff=True, is_superuser=True)
        self.teacher.set_password(password)
        self.teacher.save()
        self.course = Course(name=course_name, slug=course_slug)
        self.course.save()
        self.session = Session(course=self.course)
        self.session.save()
        self.assignment = Assignment(session=self.session)
        self.assignment.save()

    def test_add_step(self):
        '''The add_step() view creates a new step and redirect to the admin'''
        c = Client()
        c.login(username='teacher', password=password)
        self.assertEquals(self.assignment.steps.count(), 1)
        url = reverse('add_step', args=[self.course.slug, 1, 1])
        self.assertRedirects(c.get(url), reverse('admin:autodidact_step_change', args=[2]))
        self.assertEquals(self.assignment.steps.count(), 2)
