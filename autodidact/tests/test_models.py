# coding: utf-8
from __future__ import unicode_literals

import os, sys
import datetime
import shutil
from django.conf import settings
from django.test import TestCase
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from ..models import *

unicode_string = '☀☁☂☃☄★☆☇☈'
course_name = 'Test Course ☆'
course_slug = 'mtoc-psy'

class PageTest(TestCase):
    def test_content_accepts_unicode(self):
        '''The str() method returns proper utf-8 in Python 2, or proper unicode in Python 3.'''

        page = Page(slug='test', title=unicode_string)
        page.save()
        self.assertTrue(page.pk)
        page = Page.objects.get(title=unicode_string)
        page_representation = str(page)
        if sys.version_info >= (3,0,0):
            page_representation = page_representation.encode('utf-8')
        string_representation = unicode_string.encode('utf-8')
        self.assertEqual(page_representation, string_representation)

    def test_homepage_exists(self):
        '''A page with an empty slug should have been automatically created'''
        self.assertTrue(Page.objects.filter(slug='').exists())

    def test_get_absolute_url(self):
        '''The get_absolute_url() function return the 'homepage' urlpattern when the slug is empty, or the 'page' urlpattern when the slug is not empty'''

        homepage_url = reverse('homepage')
        about_page_url = reverse('page', args=['about'])
        page = Page.objects.get(slug='')
        self.assertEqual(page.get_absolute_url(), homepage_url)
        page.slug = 'about'
        self.assertEqual(page.get_absolute_url(), about_page_url)

class ProgrammeTest(TestCase):
    def test_name_accepts_unicode(self):
        '''The str() method returns proper utf-8 in Python 2, or proper unicode in Python 3.'''

        programme = Programme(name=unicode_string)
        programme.save()
        self.assertTrue(programme.pk)
        programme = Programme.objects.get(name=unicode_string)
        programme_representation = str(programme)
        if sys.version_info >= (3,0,0):
            programme_representation = programme_representation.encode('utf-8')
        string_representation = unicode_string.encode('utf-8')
        self.assertEqual(programme_representation, string_representation)

class CourseTest(TestCase):
    def setUp(self):
        self.course = Course(name=course_name, slug=course_slug)
        self.course.save()

    def test_string_representation(self):
        '''The string representation of a course object is equal to "Course name (colloquial name)"'''

        correct_representation = '{} ({})'.format(self.course.name, self.course.colloquial_name())
        if sys.version_info < (3,0,0):
            representation = unicode(self.course)
        else:
            representation = str(self.course)
        self.assertEqual(representation, correct_representation)

    def test_colloquial_name(self):
        '''The colloquial name for a course with the slug "mtoc-psy" becomes "MTO-C PSY"'''

        colloquial_name = self.course.slug.replace('-', ' ').replace('mto', 'mto-').upper()
        self.assertEqual(self.course.colloquial_name(), colloquial_name)

    def test_url_functions(self):
        '''The get_absolute_url() function returns the "course" urlpattern with the course slug as the sole argument. The url() function returns a proper <a href> hyperlink (for use in the admin).'''

        correct_url = reverse('course', args=[self.course.slug])
        correct_html = '<a href="{}">{}</a>'.format(correct_url, correct_url)
        self.assertEqual(self.course.get_absolute_url(), correct_url)
        self.assertEqual(self.course.url(), correct_html)

class SessionTest(TestCase):
    def setUp(self):
        self.course = Course(name=course_name, slug=course_slug)
        self.course.save()
        self.session1 = Session(course=self.course)
        self.session1.save()
        self.session = self.session1
        self.session2 = Session(course=self.course)
        self.session2.save()
        self.session3 = Session(course=self.course)
        self.session3.save()

    def test_string_representation(self):
        '''The string representation of a session object is equal to "Course code: Session X"'''

        representation = '{}: Session {}'.format(self.course.colloquial_name(), self.session.number)
        self.assertEqual(str(self.session), representation)

    def test_get_absolute_url(self):
        '''The absolute url of a session is the "session" urlpattern with the course slug and session number as arguments.'''

        correct_url = reverse('session', args=[
            self.course.slug,
            self.session.number,
        ])
        self.assertEqual(self.session.get_absolute_url(), correct_url)

    def test_number(self):
        '''The session number is relative: i.e. session 1 is always the first session in the queryset course.sessions'''

        self.assertEqual(self.session1.number, 1)
        self.assertEqual(self.session2.number, 2)
        self.assertEqual(self.session3.number, 3)

class AssignmentTest(TestCase):
    def setUp(self):
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

    def test_string_representation(self):
        '''The string representation of an assignment is equal to "Assignment X"'''

        representation = 'Assignment {}'.format(self.assignment.number)
        self.assertEqual(str(self.assignment), representation)

    def test_get_absolute_url(self):
        '''The absolute url of an assignment is the "assignment" urlpattern with the course slug, session number, and assignment number as arguments.'''

        correct_url = reverse('assignment', args=[
            self.course.slug,
            self.session.number,
            self.assignment.number,
        ])
        self.assertEqual(self.assignment.get_absolute_url(), correct_url)

    def test_number(self):
        '''The assignment number is relative: i.e. assignment 1 is always the first assignment in the queryset session.assignments'''

        self.assertEqual(self.assignment1.number, 1)
        self.assertEqual(self.assignment2.number, 2)
        self.assertEqual(self.assignment3.number, 3)

    def test_at_least_one_step(self):
        '''Creating an assignment also creates an associated first step'''

        self.assertIsInstance(self.assignment.steps.first(), Step)

    def test_step_count(self):
        '''The function nr_of_steps() returns the number of steps'''

        self.assertEqual(self.assignment.nr_of_steps(), 1)
        for i in range(10):
            Step(assignment=self.assignment).save()
        self.assertEqual(self.assignment.nr_of_steps(), i+2)

class StepTest(TestCase):
    def setUp(self):
        self.course = Course(name=course_name, slug=course_slug)
        self.course.save()
        self.session = Session(course=self.course)
        self.session.save()
        self.assignment = Assignment(session=self.session)
        self.assignment.save()
        self.step = self.assignment.steps.first()
        self.step1 = self.step
        self.step2 = Step(assignment=self.assignment)
        self.step2.save()
        self.step3 = Step(assignment=self.assignment)
        self.step3.save()

    def test_string_representation(self):
        '''The string representation of a step is equal to "Step X"'''

        representation = 'Step {}'.format(self.step.number)
        self.assertEqual(str(self.step), representation)

    def test_get_absolute_url(self):
        '''The absolute url of a step is the "assignment" urlpattern with the course slug, session number, and assignment number as arguments, with an additional GET parameter "step" that includes the step number'''

        correct_url = reverse('assignment', args=[
            self.course.slug,
            self.session.number,
            self.assignment.number,
        ]) + '?step=' + str(self.step.number)
        self.assertEqual(self.step.get_absolute_url(), correct_url)

    def test_number(self):
        '''The step number is relative: i.e. step 1 is always the first step in the queryset assignment.steps'''

        self.assertEqual(self.step1.number, 1)
        self.assertEqual(self.step2.number, 2)
        self.assertEqual(self.step3.number, 3)

class CompletedStepTest(TestCase):
    def setUp(self):
        self.course = Course(name=course_name, slug=course_slug)
        self.course.save()
        self.session = Session(course=self.course)
        self.session.save()
        self.assignment = Assignment(session=self.session)
        self.assignment.save()
        self.step = self.assignment.steps.first()
        self.user = get_user_model()(username='test')
        self.user.save()
        self.completedstep = CompletedStep(step=self.step, whom=self.user)

    def test_string_representation(self):
        '''A completed step is represented as "username has completed Step X"'''

        representation = "{} has completed {}".format(self.user.username, str(self.step))
        self.assertEqual(str(self.completedstep), representation)

class ClassTest(TestCase):
    def setUp(self):
        self.course = Course(name=course_name, slug=course_slug)
        self.course.save()
        self.session = Session(course=self.course)
        self.session.save()
        self.klass = Class(session=self.session, number='Testklass 1', ticket='abc')
        self.klass.save()
        for i in range(20):
            get_user_model()(username='student' + str(i)).save()
        self.klass.students = get_user_model().objects.all()
        teacher = get_user_model()(username='teacher')
        teacher.save()
        self.klass.teacher = teacher
        self.klass.save()

    def test_string_representation(self):
        '''Classes are represented as "Class X of Session Y"'''

        representation = 'Class {} of {}'.format(self.klass.number, str(self.session))
        self.assertEqual(str(self.klass), representation)

    def test_student_count(self):
        '''The function "nr_of_students()" returns the number of students.'''

        self.assertEqual(self.klass.nr_of_students(), 20)
        self.assertEqual(self.klass.nr_of_students(), self.klass.students.count())

class PathFunctionsTest(TestCase):
    def setUp(self):
        self.course = Course(name=course_name, slug=course_slug)
        self.course.save()
        self.session = Session(course=self.course)
        self.session.save()
        self.assignment = Assignment(session=self.session)
        self.assignment.save()
        self.step = self.assignment.steps.first()

    def test_session_path(self):
        '''The function session_path(), given an object and a filename, returns the relative url of the object's "session" attribute with the cleaned filename appended. E.g., session/1/filename.pdf'''

        dirty_filename = 'fílénámé.pdf☆'
        clean_filename = 'filename.pdf'
        correct_path = os.path.join(self.session.get_absolute_url()[1:], clean_filename)
        class Object:
            session = self.session
        obj = Object()
        self.assertEqual(session_path(obj, dirty_filename), correct_path)

    def test_image_path(self):
        '''The function image_path(), given an object and a filename, returns the relative url of the object's "step.assignment.session" attribute with the string "images" and the cleaned filename appended. E.g., session/1/images/filename.jpg'''

        dirty_filename = 'fílénámé.jpg☆'
        clean_filename = 'filename.jpg'
        correct_path = os.path.join(self.session.get_absolute_url()[1:], 'images', clean_filename)
        class Object:
            step = self.step
        obj = Object()
        self.assertEqual(image_path(obj, dirty_filename), correct_path)

class DownloadTest(TestCase):
    def setUp(self):
        filename = 'download.txt'
        contents = b'This file was automatically created during the unittesting of the Autodidact application. Feel free to remove it.'
        self.course = Course(name=course_name, slug=course_slug)
        self.course.save()
        self.session = Session(course=self.course)
        self.session.save()
        self.mediaroot = os.path.join(settings.MEDIA_ROOT, 'unittest' + datetime.datetime.now().isoformat())
        with self.settings(MEDIA_ROOT=self.mediaroot):
            self.download = Download(session=self.session)
            self.download.file = SimpleUploadedFile(filename, contents)
            self.download.save()

    def test_write_permissions(self):
        '''The stored file should actually exists on disk, otherwise the media directory probably doesn't have write permissions.'''

        path = os.path.join(self.mediaroot, str(self.download.file))
        self.assertTrue(os.path.isfile(path))

    def test_string_representation(self):
        '''The string representation is simply the filename'''

        self.assertEqual(str(self.download), os.path.basename(str(self.download.file)))

    def test_url(self):
        '''The url() function simply returns the file.url attribute'''

        self.assertEqual(self.download.url(), self.download.file.url)

    def tearDown(self):
        shutil.rmtree(self.mediaroot)

class PresentationTest(TestCase):
    def setUp(self):
        filename = 'presentation.txt'
        contents = b'This file was automatically created during the unittesting of the Autodidact application. Feel free to remove it.'
        self.course = Course(name=course_name, slug=course_slug)
        self.course.save()
        self.session = Session(course=self.course)
        self.session.save()
        self.mediaroot = os.path.join(settings.MEDIA_ROOT, 'unittest' + datetime.datetime.now().isoformat())
        with self.settings(MEDIA_ROOT=self.mediaroot):
            self.presentation = Presentation(session=self.session)
            self.presentation.file = SimpleUploadedFile(filename, contents)
            self.presentation.save()

    def test_write_permissions(self):
        '''The stored file should actually exists on disk, otherwise the media directory probably doesn't have write permissions.'''

        path = os.path.join(self.mediaroot, str(self.presentation.file))
        self.assertTrue(os.path.isfile(path))

    def test_string_representation(self):
        '''The string representation is simply the filename'''

        self.assertEqual(str(self.presentation), os.path.basename(str(self.presentation.file)))

    def test_url(self):
        '''The url() function simply returns the file.url attribute'''

        self.assertEqual(self.presentation.url(), self.presentation.file.url)

    def tearDown(self):
        shutil.rmtree(self.mediaroot)

class ClarificationTest(TestCase):
    def setUp(self):
        filename = 'clarification.txt'
        contents = b'This file was automatically created during the unittesting of the Autodidact application. Feel free to remove it.'
        self.course = Course(name=course_name, slug=course_slug)
        self.course.save()
        self.session = Session(course=self.course)
        self.session.save()
        self.assignment = Assignment(session=self.session)
        self.assignment.save()
        self.step = self.assignment.steps.first()
        self.mediaroot = os.path.join(settings.MEDIA_ROOT, 'unittest' + datetime.datetime.now().isoformat())
        with self.settings(MEDIA_ROOT=self.mediaroot):
            self.clarification = Clarification(step=self.step)
            self.clarification.image = SimpleUploadedFile(filename, contents)
            self.clarification.save()

    def test_string_representation(self):
        '''The string representation of a clarification is "Clarification for Step 1".'''

        representation = "Clarification for Step {}".format(self.step.number)
        self.assertEqual(str(self.clarification), representation)

    def test_write_permissions(self):
        '''The stored file should actually exists on disk, otherwise the media directory probably doesn't have write permissions.'''

        path = os.path.join(self.mediaroot, str(self.clarification.image))
        self.assertTrue(os.path.isfile(path))

    def tearDown(self):
        shutil.rmtree(self.mediaroot)
