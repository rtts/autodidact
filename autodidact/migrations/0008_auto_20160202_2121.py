# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import adminsortable.fields
import autodidact.models


class Migration(migrations.Migration):

    dependencies = [
        ('autodidact', '0007_auto_20160201_1217'),
    ]

    operations = [
        migrations.CreateModel(
            name='Presentation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.FileField(upload_to=autodidact.models.upload_path)),
                ('order', models.PositiveIntegerField(default=0, editable=False, db_index=True)),
                ('session', adminsortable.fields.SortableForeignKey(related_name='presentations', to='autodidact.Session')),
            ],
            options={
                'ordering': ['order'],
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='download',
            options={'ordering': ['file']},
        ),
        migrations.RemoveField(
            model_name='download',
            name='session',
        ),
        migrations.AlterField(
            model_name='download',
            name='file',
            field=models.FileField(upload_to=autodidact.models.upload_path),
            preserve_default=True,
        ),
    ]
