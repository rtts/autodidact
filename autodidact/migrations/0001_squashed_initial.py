# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autodidact.models
import pandocfield.fields
from django.conf import settings


class Migration(migrations.Migration):

    replaces = [('autodidact', '0001_initial'), ('autodidact', '0002_auto_20160126_1520'), ('autodidact', '0003_auto_20160130_0030'), ('autodidact', '0004_auto_20160201_0848'), ('autodidact', '0005_auto_20160201_0854'), ('autodidact', '0006_auto_20160201_0909'), ('autodidact', '0007_auto_20160201_1217'), ('autodidact', '0008_auto_20160202_2121'), ('autodidact', '0009_download_session'), ('autodidact', '0010_presentation_visibility'), ('autodidact', '0011_auto_20160202_2233'), ('autodidact', '0012_auto_20160209_1151'), ('autodidact', '0013_auto_20160223_2152'), ('autodidact', '0014_auto_20160224_1544'), ('autodidact', '0015_auto_20160307_0849'), ('autodidact', '0016_auto_20160307_0855'), ('autodidact', '0017_page'), ('autodidact', '0018_auto_20160309_1223'), ('autodidact', '0019_auto_20160329_1123'), ('autodidact', '0002_rename_order_to_number'), ('autodidact', '0003_new_models_and_fields'), ('autodidact', '0004_resave_all_text_fields')]

    dependencies = [
        ('contenttypes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('number', models.PositiveIntegerField(blank=True)),
                ('name', models.CharField(blank=True, max_length=255)),
                ('active', models.BooleanField(default=False, help_text='Inactive assignments are not visible to students')),
                ('locked', models.BooleanField(default=True, help_text='Locked assignments can only be made by students in class')),
            ],
            options={
                'ordering': ['number'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Clarification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('description', pandocfield.fields.PandocField(blank=True, auto_create_html_field=False)),
                ('image', models.ImageField(blank=True)),
                ('_description_html', models.TextField(editable=False, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('number', models.CharField(max_length=16)),
                ('ticket', models.CharField(max_length=16, unique=True)),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('order', models.PositiveIntegerField(blank=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
                ('description', pandocfield.fields.PandocField(blank=True, auto_create_html_field=False)),
                ('active', models.BooleanField(default=True, help_text='Inactive courses are not visible to students')),
                ('_description_html', models.TextField(editable=False, blank=True)),
            ],
            options={
                'ordering': ['order'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Download',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('file', models.FileField()),
            ],
            options={
                'ordering': ['file'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('slug', models.SlugField(unique=True, help_text='Leave this field blank for the homepage', blank=True)),
                ('title', models.CharField(blank=True, max_length=255)),
                ('content', pandocfield.fields.PandocField(blank=True, auto_create_html_field=False)),
                ('_content_html', models.TextField(editable=False, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Presentation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('file', models.FileField()),
                ('visibility', models.IntegerField(default=1, choices=[(1, 'Only visible to teacher'), (2, 'Visible to students in class'), (3, 'Visible to everyone')])),
            ],
            options={
                'ordering': ['file'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Programme',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('number', models.PositiveIntegerField(blank=True)),
                ('name', models.CharField(blank=True, max_length=255)),
                ('description', pandocfield.fields.PandocField(blank=True, auto_create_html_field=False)),
                ('_description_html', models.TextField(editable=False, blank=True)),
                ('registration_enabled', models.BooleanField(default=True, help_text='When enabled, class attendance will be registered')),
                ('active', models.BooleanField(default=True, help_text='Inactive sessions are not visible to students')),
                ('course', models.ForeignKey(related_name='sessions', to='autodidact.Course')),
            ],
            options={
                'ordering': ['number'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Step',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('number', models.PositiveIntegerField(blank=True)),
                ('description', pandocfield.fields.PandocField(blank=True, auto_create_html_field=False)),
                ('answer_required', models.BooleanField(default=False, help_text='If enabled, this step will show the student a text box where they can enter their answer')),
                ('_description_html', models.TextField(editable=False, blank=True)),
                ('assignment', models.ForeignKey(related_name='steps', to='autodidact.Assignment')),
            ],
            options={
                'ordering': ['number'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('number', models.PositiveIntegerField(blank=True)),
                ('name', models.CharField(blank=True, max_length=255)),
                ('description', pandocfield.fields.PandocField(blank=True, auto_create_html_field=False)),
                ('_description_html', models.TextField(editable=False, blank=True)),
                ('course', models.ForeignKey(related_name='topics', to='autodidact.Course')),
            ],
            options={
                'ordering': ['number'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='presentation',
            name='session',
            field=models.ForeignKey(related_name='presentations', to='autodidact.Session'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='download',
            name='session',
            field=models.ForeignKey(related_name='downloads', to='autodidact.Session'),
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
            field=models.ForeignKey(related_name='completed', to='autodidact.Step'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='completedstep',
            name='whom',
            field=models.ForeignKey(related_name='completed', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='class',
            name='session',
            field=models.ForeignKey(related_name='classes', to='autodidact.Session'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='class',
            name='students',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, related_name='attends'),
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
            field=models.ForeignKey(related_name='clarifications', to='autodidact.Step'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assignment',
            name='session',
            field=models.ForeignKey(related_name='assignments', to='autodidact.Session'),
            preserve_default=True,
        ),
    ]
