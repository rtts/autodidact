# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autodidact', '0013_auto_20160223_2152'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignment',
            name='type',
        ),
        migrations.AlterField(
            model_name='assignment',
            name='locked',
            field=models.BooleanField(default=True, help_text=b'Locked assignments can only be made by students in class'),
            preserve_default=True,
        ),
    ]
