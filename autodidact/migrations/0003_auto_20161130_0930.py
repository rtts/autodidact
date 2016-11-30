# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import pandocfield.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('autodidact', '0002_auto_20161004_1251'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompletedQuiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'completed quizzes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(blank=True)),
                ('description', pandocfield.fields.PandocField(auto_create_html_field=False, blank=True)),
                ('_description_html', models.TextField(editable=False, blank=True)),
            ],
            options={
                'ordering': ['number'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=False)),
                ('locked', models.BooleanField(default=True)),
                ('course', models.ForeignKey(to='autodidact.Course', related_name='quizzes')),
            ],
            options={
                'verbose_name_plural': 'quizzes',
                'ordering': ['pk'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RightAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=255)),
                ('question', models.ForeignKey(to='autodidact.Question', related_name='right_answers')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WrongAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=255)),
                ('question', models.ForeignKey(to='autodidact.Question', related_name='wrong_answers')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='question',
            name='quiz',
            field=models.ForeignKey(to='autodidact.Quiz', related_name='questions'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='completedquiz',
            name='quiz',
            field=models.ForeignKey(to='autodidact.Question', related_name='answers'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='completedquiz',
            name='whom',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='answers'),
            preserve_default=True,
        ),
    ]
