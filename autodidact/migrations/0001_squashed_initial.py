# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autodidact.models
from django.conf import settings

class Migration(migrations.Migration):

    replaces = [('autodidact', '0001_initial'), ('autodidact', '0002_auto_20160126_1520'), ('autodidact', '0003_auto_20160130_0030'), ('autodidact', '0004_auto_20160201_0848'), ('autodidact', '0005_auto_20160201_0854'), ('autodidact', '0006_auto_20160201_0909'), ('autodidact', '0007_auto_20160201_1217'), ('autodidact', '0008_auto_20160202_2121'), ('autodidact', '0009_download_session'), ('autodidact', '0010_presentation_visibility'), ('autodidact', '0011_auto_20160202_2233'), ('autodidact', '0012_auto_20160209_1151'), ('autodidact', '0013_auto_20160223_2152'), ('autodidact', '0014_auto_20160224_1544'), ('autodidact', '0015_auto_20160307_0849'), ('autodidact', '0016_auto_20160307_0855'), ('autodidact', '0017_page'), ('autodidact', '0018_auto_20160309_1223'), ('autodidact', '0019_auto_20160329_1123')]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, blank=True)),
                ('active', models.BooleanField(help_text='Inactive assignments are not visible to students', default=False)),
                ('locked', models.BooleanField(help_text='Locked assignments can only be made by students in class', default=True)),
                ('order', models.PositiveIntegerField(editable=False, default=0, db_index=True)),
            ],
            options={
                'ordering': ['order'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Clarification',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('description', models.TextField(help_text='This field supports <a target="_blank" href="http://daringfireball.net/projects/markdown/syntax">Markdown syntax</a>')),
                ('image', models.ImageField(upload_to=autodidact.models.image_path)),
                ('order', models.PositiveIntegerField(editable=False, default=0, db_index=True)),
            ],
            options={
                'ordering': ['order'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('number', models.CharField(max_length=16)),
                ('ticket', models.CharField(unique=True, max_length=16)),
                ('dismissed', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'classes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CompletedStep',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('answer', models.TextField(blank=True)),
            ],
            options={
                'verbose_name_plural': 'completed steps',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
                ('description', models.TextField(help_text='This field supports <a target="_blank" href="http://daringfireball.net/projects/markdown/syntax">Markdown syntax</a>')),
                ('active', models.BooleanField(help_text='Inactive courses are not visible to students', default=True)),
                ('order', models.PositiveIntegerField(editable=False, default=0, db_index=True)),
            ],
            options={
                'ordering': ['order'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Download',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('file', models.FileField(upload_to=autodidact.models.session_path)),
            ],
            options={
                'ordering': ['file'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('slug', models.SlugField(unique=True, blank=True)),
                ('content', models.TextField(help_text='This field supports <a target="_blank" href="http://daringfireball.net/projects/markdown/syntax">Markdown syntax</a>')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Presentation',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('file', models.FileField(upload_to=autodidact.models.session_path)),
                ('visibility', models.IntegerField(choices=[(1, 'Only visible to teacher'), (2, 'Visible to students in class'), (3, 'Visible to everyone')], default=1)),
                ('order', models.PositiveIntegerField(editable=False, default=0, db_index=True)),
            ],
            options={
                'ordering': ['order'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Programme',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, blank=True)),
                ('description', models.TextField(help_text='This field supports <a target="_blank" href="http://daringfireball.net/projects/markdown/syntax">Markdown syntax</a>', blank=True)),
                ('registration_enabled', models.BooleanField(help_text='When enabled, class attendance will be registered', default=True)),
                ('active', models.BooleanField(help_text='Inactive sessions are not visible to students', default=True)),
                ('order', models.PositiveIntegerField(editable=False, default=0, db_index=True)),
                ('course', models.ForeignKey(to='autodidact.Course', related_name='sessions')),
            ],
            options={
                'ordering': ['order'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Step',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, blank=True)),
                ('description', models.TextField(help_text='This field supports <a target="_blank" href="http://daringfireball.net/projects/markdown/syntax">Markdown syntax</a>', blank=True)),
                ('answer_required', models.BooleanField(help_text='If enabled, this step will show the student a text box where they can enter their answer', default=False)),
                ('order', models.PositiveIntegerField(editable=False, default=0, db_index=True)),
                ('assignment', models.ForeignKey(to='autodidact.Assignment', related_name='steps')),
            ],
            options={
                'ordering': ['order'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='presentation',
            name='session',
            field=models.ForeignKey(to='autodidact.Session', related_name='presentations'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='download',
            name='session',
            field=models.ForeignKey(to='autodidact.Session', related_name='downloads'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='course',
            name='programmes',
            field=models.ManyToManyField(to='autodidact.Programme', related_name='courses'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='completedstep',
            name='step',
            field=models.ForeignKey(to='autodidact.Step', related_name='completed'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='completedstep',
            name='whom',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='completed'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='class',
            name='session',
            field=models.ForeignKey(to='autodidact.Session', related_name='classes'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='class',
            name='students',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='attends', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='class',
            name='teacher',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, null=True, related_name='teaches'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='clarification',
            name='step',
            field=models.ForeignKey(to='autodidact.Step', related_name='clarifications'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assignment',
            name='session',
            field=models.ForeignKey(to='autodidact.Session', related_name='assignments'),
            preserve_default=True,
        ),
    ]
