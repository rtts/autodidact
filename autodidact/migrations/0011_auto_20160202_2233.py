# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autodidact', '0010_presentation_visibility'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='registration_enabled',
            field=models.BooleanField(default=True, help_text=b'When enabled, class attendance will be registered and the teacher will be able to track the progress of individual students'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='step',
            name='answer_required',
            field=models.BooleanField(default=False, help_text=b'If enabled, this step will show the student a text box where they can enter their answer'),
            preserve_default=True,
        ),
    ]
