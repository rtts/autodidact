# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

from django.db import migrations
import sys

def resave_all_text_fields(apps, schema_editor):

    # This migration doesn't reference any historical fields, so
    # directly importing these should be safe
    from autodidact.models import Assignment, Clarification, Course, Page, Session, Step, Topic

    print('''
    To make sure all existing data conforms to Autodidact 1.0
    and up, all objects will now be re-saved. This will trigger both
    the (re)numbering and HTML (re)generation methods.
    ''')

    for klass in [Assignment, Clarification, Course, Page, Session, Step, Topic]:
        print("    Re-saving {}s: ".format(klass.__name__), end='')
        for obj in klass.objects.all():
            sys.stdout.write('.')
            sys.stdout.flush()
            obj.save()
        else:
            print(' done')
        if obj is None:
            print('(none exist)')
    print()

def noop(*args):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('autodidact', '0003_new_models_and_fields'),
    ]

    operations = [
        migrations.RunPython(resave_all_text_fields, noop),
    ]
