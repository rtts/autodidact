# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autodidact', '0008_auto_20170103_1439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='completedquiz',
            name='quiz',
            field=models.ForeignKey(related_name='completed_quizzes', to='autodidact.Quiz'),
            preserve_default=True,
        ),
    ]
