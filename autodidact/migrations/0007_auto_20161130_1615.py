# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('autodidact', '0006_quizfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='completedquiz',
            name='quiz',
            field=models.ForeignKey(related_name='completed_quizzes', to='autodidact.Question'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='completedquiz',
            name='whom',
            field=models.ForeignKey(related_name='completed_quizzes', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
