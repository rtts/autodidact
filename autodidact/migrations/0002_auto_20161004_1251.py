# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autodidact', '0001_squashed_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='clarification',
            options={'ordering': ['number']},
        ),
        migrations.AddField(
            model_name='clarification',
            name='number',
            field=models.PositiveIntegerField(default=1, blank=True),
            preserve_default=False,
        ),
    ]
