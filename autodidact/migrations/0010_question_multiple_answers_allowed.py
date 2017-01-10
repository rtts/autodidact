# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autodidact', '0009_auto_20170103_1614'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='multiple_answers_allowed',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
