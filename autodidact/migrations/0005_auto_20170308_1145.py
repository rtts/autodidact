# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autodidact', '0004_completedstep_passed'),
    ]

    operations = [
        migrations.AddField(
            model_name='programme',
            name='order',
            field=models.PositiveIntegerField(blank=True, default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='assignment',
            name='active',
            field=models.BooleanField(help_text='Inactive assignments are not visible to students', default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='assignment',
            name='session',
            field=models.ForeignKey(help_text='You can move assignments between sessions by using this dropdown menu', related_name='assignments', to='autodidact.Session'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='presentation',
            name='visibility',
            field=models.IntegerField(default=1, choices=[(0, 'Invisible'), (1, 'Only visible to teacher'), (2, 'Visible to students in class'), (3, 'Visible to everyone')]),
            preserve_default=True,
        ),
    ]
