# coding: utf-8
import sys
from django.test import TestCase
from django.utils import timezone
from django.core.urlresolvers import reverse
from ..models import *

unicode_string = u'☀☁☂☃☄★☆☇☈'

class PageTest(TestCase):
    def test_content_accepts_unicode(self):
        '''This test stores and retrieves a Page object with unicode
        characters in the "content" field. It then checks if the str() method
        returns proper utf-8 in Python 2, or proper unicode in Python 3.'''

        page = Page(slug='', content=unicode_string)
        page.save()
        self.assertTrue(page.pk)
        page = Page.objects.get(content=unicode_string)
        page_representation = str(page)
        if sys.version_info >= (3,0,0):
            page_representation = page_representation.encode('utf-8')
        string_representation = unicode_string.encode('utf-8')
        self.assertEqual(page_representation, string_representation)

    def test_get_absolute_url(self):
        '''Tests the get_absolute_url() function. Requires that the urls
        named 'homepage' and 'page' are defined in urls.py'''

        homepage_url = reverse('homepage')
        about_page_url = reverse('page', args=['about'])
        page = Page(slug='', content='X')
        self.assertEqual(page.get_absolute_url(), homepage_url)
        page.slug = 'about'
        self.assertEqual(page.get_absolute_url(), about_page_url)

class ProgrammeTest(TestCase):
    def test_name_accepts_unicode(self):
        '''This test stores and retrieves a Programme object with unicode
        characters in the "content" field. It then checks if the str() method
        returns proper utf-8 in Python 2, or proper unicode in Python 3.'''

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
    def test_string_representation(self):
        '''A simple test to verify that the string representation of a course
        object is equal to "Course name (colloquial name)"'''

        course_name = 'Test Course'
        course_slug = 'TC'
        representation = '{} ({})'.format(course_name, course_slug)
        course = Course(name=course_name, slug=course_slug)
        self.assertEqual(str(course), representation)

    def test_colloquial_name(self):
        '''Verifies that the colloquial course name for slug "mtoc-psy"
        becomes "MTO-C PSY"'''

        course_name = 'Test Course'
        course_slug = 'mtoc-psy'
        colloquial_name = 'MTO-C PSY'
        course = Course(name=course_name, slug=course_slug)
        self.assertEqual(course.colloquial_name(), colloquial_name)

    def test_get_absolute_url(self):
        '''The absolute url of a course should be the "course" url with the
        course slug as the sole argument'''

        course_name = 'Test Course'
        course_slug = 'mtoc-psy'
        correct_url = reverse('course', args=[course_slug])
        course = Course(name=course_name, slug=course_slug)
        self.assertEqual(course.get_absolute_url(), correct_url)

class SessionTest(TestCase):
    def test_string_representation(self):
        '''A simple test to verify that the string representation of a session
        object is equal to "Course code: Session X"'''

        course_name = 'Test Course'
        course_slug = 'mtoc-psy'
        course = Course(name=course_name, slug=course_slug)
        course.save()
        session = Session(course=course)
        session.save()
        representation = '{}: Session {}'.format(course.colloquial_name(), session.get_number())
        self.assertEqual(str(session), representation)

    def test_get_absolute_url(self):
        '''The absolute url of a session should be the "session" url with the
        course slug and session number as arguments'''

        course_name = 'Test Course'
        course_slug = 'mtoc-psy'
        course = Course(name=course_name, slug=course_slug)
        course.save()
        session = Session(course=course)
        session.save()
        correct_url = reverse('session', args=[course_slug, session.get_number()])
        self.assertEqual(session.get_absolute_url(), correct_url)

    def test_get_number(self):
        '''The session number should be relative: i.e. session 1 is always the
        first session in the queryset course.sessions'''

        course_name = 'Test Course'
        course_slug = 'mtoc-psy'
        course = Course(name=course_name, slug=course_slug)
        course.save()
        session1 = Session(course=course)
        session1.save()
        session2 = Session(course=course)
        session2.save()
        session3 = Session(course=course)
        session3.save()
        self.assertEqual(session1.get_number(), 1)
        self.assertEqual(session2.get_number(), 2)
        self.assertEqual(session3.get_number(), 3)
