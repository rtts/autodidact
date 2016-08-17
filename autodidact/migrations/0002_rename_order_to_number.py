# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

class Migration(migrations.Migration):
    '''This migration ensures the new number fields retain their existing order numbers. Without it, all order would be lost.'''

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('autodidact', '0001_squashed_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='session',
            old_name='order',
            new_name='number',
        ),
        migrations.RenameField(
            model_name='assignment',
            old_name='order',
            new_name='number',
        ),
        migrations.RenameField(
            model_name='step',
            old_name='order',
            new_name='number',
        ),
    ]
