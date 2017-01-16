# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autodidact', '0002_auto_20161004_1251'),
    ]

    operations = [
        migrations.CreateModel(
            name='RightAnswer',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('value', models.CharField(help_text='This value can either be a case-insensitive string or a numeric value. For numeric values you can use the <a target="_blank" href="https://docs.moodle.org/23/en/GIFT_format">GIFT notation</a> of "answer:tolerance" or "low..high".', max_length=255)),
                ('step', models.ForeignKey(related_name='right_answers', to='autodidact.Step')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WrongAnswer',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('value', models.CharField(help_text='Supplying one or more wrong answers will turn this into a multiple choice question.', max_length=255)),
                ('step', models.ForeignKey(related_name='wrong_answers', to='autodidact.Step')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='course',
            name='slug',
            field=models.SlugField(unique=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='step',
            name='answer_required',
            field=models.BooleanField(default=False, help_text='If enabled, this step will show students an input field where they can enter their answer. Add one or more right answers below to have students’ answers checked for correctness.'),
            preserve_default=True,
        ),
    ]
