# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autodidact', '0008_auto_20160202_2121'),
    ]

    operations = [
        migrations.AddField(
            model_name='download',
            name='session',
            field=models.ForeignKey(related_name='downloads', default=1, to='autodidact.Session'),
            preserve_default=False,
        ),
    ]
