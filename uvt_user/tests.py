# coding: utf-8
from __future__ import unicode_literals
import os, sys, six
if six.PY2:
    import mock
if six.PY3:
    from unittest import mock
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import *
from .utils import *

name = "毛泽东"

class ModelTest(TestCase):
    def setUp(self):
        self.uvt_user = UvtUser(full_name=name)

    def test_string_representation(self):
        '''The string representation of a Uvt User is the full name, unicode characters allowed.'''
        if sys.version_info < (3,0,0):
            representation = unicode(self.uvt_user)
        else:
            representation = str(self.uvt_user)
        self.assertEqual(representation, name)

class LdapTest(TestCase):
    @mock.patch('uvt_user.utils.Server')
    @mock.patch('uvt_user.utils.Connection')
    def test_search_ldap(self, Connection, Server):
        '''The search_ldap() function instantiates Server() and Connection() objects, and calls the search() function with the username as a search filter. On error it throws an LDAPError.'''
        conn = Connection.return_value = mock.MagicMock()
        search_ldap(name)
        self.assertTrue(Server.called)
        self.assertTrue(Connection.called)
        (args, kwargs) = conn.search.call_args
        self.assertTrue(args[1] == '(uid={})'.format(name))

        Connection.side_effect = Exception
        with self.assertRaises(LDAPError):
            search_ldap(name)
