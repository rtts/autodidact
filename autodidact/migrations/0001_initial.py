# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import adminsortable.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('order', models.PositiveIntegerField(default=0, editable=False, db_index=True)),
                ('answer_required', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['order'],
                'verbose_name_plural': 'activities',
            },
        ),
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('order', models.PositiveIntegerField(default=0, editable=False, db_index=True)),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='CompletedActivity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('answer', models.TextField(blank=True)),
                ('activity', models.ForeignKey(to='autodidact.Activity')),
                ('whom', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'completed activities',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
                ('description', models.TextField()),
                ('order', models.PositiveIntegerField(default=0, editable=False, db_index=True)),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Download',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('file', models.FileField(upload_to=b'', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Programme',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('order', models.PositiveIntegerField(default=0, editable=False, db_index=True)),
                ('course', adminsortable.fields.SortableForeignKey(related_name='sessions', to='autodidact.Course')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.AddField(
            model_name='download',
            name='session',
            field=models.ManyToManyField(related_name='downloads', to='autodidact.Session'),
        ),
        migrations.AddField(
            model_name='course',
            name='programmes',
            field=models.ManyToManyField(related_name='courses', to='autodidact.Programme'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='session',
            field=adminsortable.fields.SortableForeignKey(related_name='assignments', to='autodidact.Session'),
        ),
        migrations.AddField(
            model_name='activity',
            name='assignment',
            field=adminsortable.fields.SortableForeignKey(related_name='activities', to='autodidact.Assignment'),
        ),
    ]
