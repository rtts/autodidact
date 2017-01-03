# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autodidact', '0007_auto_20161130_1615'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question',
            options={'verbose_name': 'quiz question', 'ordering': ['number']},
        ),
        migrations.AlterField(
            model_name='course',
            name='slug',
            field=models.SlugField(unique=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='rightanswer',
            name='value',
            field=models.CharField(help_text='This value can either be a case-insensitive string or a numeric value. For numeric values you can use the <a target="_blank" href="https://docs.moodle.org/23/en/GIFT_format">GIFT notation</a> of "answer:tolerance" or "low..high".', max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='wronganswer',
            name='value',
            field=models.CharField(help_text='Supplying one or more wrong answers will automatically turn the question into a multiple choice question.', max_length=255),
            preserve_default=True,
        ),
    ]
