# coding: utf-8
from __future__ import unicode_literals
import sys
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import UvtUser
from .utils import search_ldap

class ModelTest(TestCase):
    def setUp(self):
        self.uvt_user = UvtUser(full_name='毛泽东')

    def test_string_representation(self):
        '''The string representation of a Uvt User is the full name, unicode characters allowed.'''
        if sys.version_info < (3,0,0):
            representation = unicode(self.uvt_user)
        else:
            representation = str(self.uvt_user)
        self.assertEqual(representation, '毛泽东')

class LdapTest(TestCase):
    def test_search_ldap(self):
        '''The search_ldap() returns a 4-tuple of first name, full name, ANR, and email'''
        (first_name, full_name, ANR, email) = search_ldap('jvens')

        # This test fails unless the original author is employed at Tilburg University
        self.assertEqual(first_name, 'Jaap Joris')
        self.assertEqual(full_name, 'J.J. Vens')
        self.assertEqual(ANR, '682051')
        self.assertEqual(email, 'J.J.Vens@uvt.nl')

class SignalsTest(TestCase):
    def test_auto_populate_uvt_user(self):
        '''Saving a Django user triggers the creation of an associated Uvt User'''
        user = get_user_model()(username='jvens')
        user.save()

        # This test fails unless the original author is employed at Tilburg University
        self.assertEqual(user.uvt_user.first_name, 'Jaap Joris')
        self.assertEqual(user.uvt_user.full_name, 'J.J. Vens')
        self.assertEqual(user.uvt_user.ANR, '682051')
        self.assertEqual(user.uvt_user.email, 'J.J.Vens@uvt.nl')
