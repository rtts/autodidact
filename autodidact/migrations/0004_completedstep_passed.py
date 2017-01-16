# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autodidact', '0003_auto_20170116_1142'),
    ]

    operations = [
        migrations.AddField(
            model_name='completedstep',
            name='passed',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
