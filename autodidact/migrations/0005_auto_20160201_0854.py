# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import adminsortable.fields


class Migration(migrations.Migration):

    dependencies = [
        ('autodidact', '0004_auto_20160201_0848'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='class',
            options={'verbose_name_plural': 'classes'},
        ),
        migrations.AlterModelOptions(
            name='completedstep',
            options={'verbose_name_plural': 'completed steps'},
        ),
        migrations.AlterModelOptions(
            name='step',
            options={'ordering': ['order']},
        ),
        migrations.RenameField(
            model_name='completedstep',
            old_name='activity',
            new_name='step',
        ),
        migrations.RenameField(
            model_name='session',
            old_name='attendance_required',
            new_name='registration_enabled',
        ),
        migrations.AlterField(
            model_name='session',
            name='registration_enabled',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='class',
            name='session',
            field=models.ForeignKey(related_name='classes', to='autodidact.Session'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='course',
            name='description',
            field=models.TextField(help_text=b'This field supports <a target="_blank" href="http://daringfireball.net/projects/markdown/syntax">Markdown syntax</a>'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='session',
            name='description',
            field=models.TextField(help_text=b'This field supports <a target="_blank" href="http://daringfireball.net/projects/markdown/syntax">Markdown syntax</a>'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='step',
            name='assignment',
            field=adminsortable.fields.SortableForeignKey(related_name='steps', to='autodidact.Assignment'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='step',
            name='description',
            field=models.TextField(help_text=b'This field supports <a target="_blank" href="http://daringfireball.net/projects/markdown/syntax">Markdown syntax</a>'),
            preserve_default=True,
        ),
    ]
