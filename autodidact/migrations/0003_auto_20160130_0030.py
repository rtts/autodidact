# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('autodidact', '0002_auto_20160126_1520'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.CharField(max_length=16)),
                ('ticket', models.CharField(unique=True, max_length=16)),
                ('session', models.ForeignKey(related_name='groups', to='autodidact.Session')),
                ('users', models.ManyToManyField(related_name='attends', to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='assignment',
            name='locked_until_class_starts',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assignment',
            name='type',
            field=models.IntegerField(default=1, choices=[(1, b'Homework assignment'), (2, b'In-class assignment')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='session',
            name='attendance_required',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
