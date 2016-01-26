# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('autodidact', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='download',
            name='description',
        ),
        migrations.RemoveField(
            model_name='download',
            name='name',
        ),
        migrations.AlterField(
            model_name='completedactivity',
            name='whom',
            field=models.ForeignKey(related_name='completed', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='download',
            name='file',
            field=models.FileField(upload_to=b''),
            preserve_default=True,
        ),
    ]
