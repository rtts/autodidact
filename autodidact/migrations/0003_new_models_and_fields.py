# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import pandocfield.fields
import autodidact.models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('autodidact', '0002_rename_order_to_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(unique=True, max_length=255)),
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
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('number', models.PositiveIntegerField(blank=True)),
                ('name', models.CharField(max_length=255, blank=True)),
                ('description', pandocfield.fields.PandocField(auto_create_html_field=False, blank=True)),
                ('_description_html', models.TextField(editable=False, blank=True)),
                ('course', models.ForeignKey(to='autodidact.Course', related_name='topics')),
            ],
            options={
                'ordering': ['number'],
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='assignment',
            options={'ordering': ['number']},
        ),
        migrations.AlterModelOptions(
            name='clarification',
            options={},
        ),
        migrations.AlterModelOptions(
            name='presentation',
            options={'ordering': ['file']},
        ),
        migrations.AlterModelOptions(
            name='session',
            options={'ordering': ['number']},
        ),
        migrations.AlterModelOptions(
            name='step',
            options={'ordering': ['number']},
        ),
        migrations.RemoveField(
            model_name='clarification',
            name='order',
        ),
        migrations.RemoveField(
            model_name='presentation',
            name='order',
        ),
        migrations.RemoveField(
            model_name='step',
            name='name',
        ),
        migrations.AddField(
            model_name='clarification',
            name='_description_html',
            field=models.TextField(editable=False, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='course',
            name='_description_html',
            field=models.TextField(editable=False, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='page',
            name='_content_html',
            field=models.TextField(editable=False, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='page',
            name='title',
            field=models.CharField(max_length=255, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='session',
            name='_description_html',
            field=models.TextField(editable=False, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='step',
            name='_description_html',
            field=models.TextField(editable=False, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='assignment',
            name='number',
            field=models.PositiveIntegerField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clarification',
            name='description',
            field=pandocfield.fields.PandocField(auto_create_html_field=False, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clarification',
            name='image',
            field=models.ImageField(upload_to=autodidact.models.image_path, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='course',
            name='description',
            field=pandocfield.fields.PandocField(auto_create_html_field=False, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='course',
            name='order',
            field=models.PositiveIntegerField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='page',
            name='content',
            field=pandocfield.fields.PandocField(auto_create_html_field=False, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='page',
            name='slug',
            field=models.SlugField(unique=True, help_text='Leave this field blank for the homepage', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='session',
            name='description',
            field=pandocfield.fields.PandocField(auto_create_html_field=False, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='session',
            name='number',
            field=models.PositiveIntegerField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='step',
            name='description',
            field=pandocfield.fields.PandocField(auto_create_html_field=False, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='step',
            name='number',
            field=models.PositiveIntegerField(blank=True),
            preserve_default=True,
        ),
    ]
