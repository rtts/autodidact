# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autodidact', '0006_auto_20160201_0909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='type',
            field=models.IntegerField(choices=[(1, b'Preliminary assignment'), (2, b'In-class assignment')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='download',
            name='session',
            field=models.ManyToManyField(related_name='downloads', to='autodidact.Session', blank=True),
            preserve_default=True,
        ),
    ]
