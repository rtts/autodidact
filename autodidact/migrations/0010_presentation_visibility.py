# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autodidact', '0009_download_session'),
    ]

    operations = [
        migrations.AddField(
            model_name='presentation',
            name='visibility',
            field=models.IntegerField(default=1, choices=[(1, b'Only visible to teacher'), (2, b'Visible to students in class'), (3, b'Visible to everyone')]),
            preserve_default=False,
        ),
    ]
