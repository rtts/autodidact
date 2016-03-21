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
        self.page = Page(slug='', content=unicode_string)
        self.page.save()
        self.programme = Programme(name=unicode_string)
        self.programme.save()

    def test_page_view(self):
        c = Client()
        c.login(username=username, password=password)
        url = reverse('homepage')
        response = c.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['page'], self.page)
        self.assertQuerysetEqual(response.context['programmes'], map(repr, Programme.objects.all()))

class CourseViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model()(username=username)
        self.user.set_password(password)
        self.user.save()
        self.course = Course(name=course_name, slug=course_slug)
        self.course.save()

    def test_course_view(self):
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
        self.klass = Class(session=self.session, ticket=self.valid_ticket)
        self.klass.save()

    def test_context_variables(self):
        c = Client()
        c.login(username=username, password=password)
        url = reverse('session', args=[course_slug, '1'])
        response = c.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['course'], self.course)
        self.assertEqual(response.context['session'], self.session)
        self.assertQuerysetEqual(response.context['assignments'], map(repr, self.session.assignments.all()))

    def test_post_ticket(self):
        c = Client()
        c.login(username=username, password=password)
        url = reverse('session', args=[course_slug, '1'])
        response = c.post(url, {'ticket': self.invalid_ticket})
        self.assertEqual(response.context['ticket_error'], self.invalid_ticket)
        response = c.post(url, {'ticket': self.valid_ticket})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.endswith(url))

    def test_students_and_teacher(self):
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
