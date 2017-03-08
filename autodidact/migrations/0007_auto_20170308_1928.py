# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autodidact', '0006_auto_20170308_1203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='active',
            field=models.BooleanField(help_text='Inactive assignments are not visible to students', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='assignment',
            name='locked',
            field=models.BooleanField(help_text='Locked assignments can only be made by students in class', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='course',
            name='active',
            field=models.BooleanField(help_text='Inactive courses are not visible to students', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='session',
            name='active',
            field=models.BooleanField(help_text='Inactive sessions are not visible to students', default=False),
            preserve_default=True,
        ),
    ]
