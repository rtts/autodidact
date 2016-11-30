# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autodidact.models


class Migration(migrations.Migration):

    dependencies = [
        ('autodidact', '0005_auto_20161130_1249'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuizFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('file', models.FileField(upload_to=autodidact.models.course_path)),
                ('quiz', models.ForeignKey(related_name='files', to='autodidact.Quiz')),
            ],
            options={
                'ordering': ['file'],
            },
            bases=(models.Model,),
        ),
    ]
