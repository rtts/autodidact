# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
import autodidact.models


class Migration(migrations.Migration):

    dependencies = [
        ('autodidact', '0012_auto_20160209_1151'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clarification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField(help_text=b'This field supports <a target="_blank" href="http://daringfireball.net/projects/markdown/syntax">Markdown syntax</a>')),
                ('image', models.ImageField(upload_to=autodidact.models.image_path)),
                ('order', models.PositiveIntegerField(default=0, editable=False, db_index=True)),
                ('step', models.ForeignKey(related_name='clarifications', to='autodidact.Step')),
            ],
            options={
                'ordering': ['order'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='class',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 23, 21, 52, 59, 722396, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='class',
            name='dismissed',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='assignment',
            name='locked',
            field=models.BooleanField(default=False, help_text=b'Locked assignments will automatically unlock when students register their attendance to class'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='session',
            name='registration_enabled',
            field=models.BooleanField(default=True, help_text=b'When enabled, class attendance will be registered'),
            preserve_default=True,
        ),
    ]
