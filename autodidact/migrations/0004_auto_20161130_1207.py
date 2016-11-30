# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autodidact', '0003_auto_20161130_0930'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='quiz',
            options={'verbose_name_plural': 'quizzes', 'ordering': ['number']},
        ),
        migrations.AddField(
            model_name='quiz',
            name='number',
            field=models.PositiveIntegerField(default=1, blank=True),
            preserve_default=False,
        ),
    ]
