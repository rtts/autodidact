# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import autodidact.models


class Migration(migrations.Migration):

    dependencies = [
        ('autodidact', '0004_auto_20161130_1207'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiz',
            name='active',
        ),
        migrations.RemoveField(
            model_name='quiz',
            name='locked',
        ),
        migrations.AddField(
            model_name='course',
            name='quiz_from',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Quiz available from'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='course',
            name='quiz_until',
            field=models.DateTimeField(default=autodidact.models.week_later, verbose_name='Quiz available until'),
            preserve_default=True,
        ),
    ]
