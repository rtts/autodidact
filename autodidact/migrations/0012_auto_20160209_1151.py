# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autodidact', '0011_auto_20160202_2233'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='active',
            field=models.BooleanField(default=True, help_text=b'Inactive assignments are not visible to students'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='course',
            name='active',
            field=models.BooleanField(default=True, help_text=b'Inactive courses are not visible to students'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='session',
            name='active',
            field=models.BooleanField(default=True, help_text=b'Inactive sessions are not visible to students'),
            preserve_default=True,
        ),
    ]
