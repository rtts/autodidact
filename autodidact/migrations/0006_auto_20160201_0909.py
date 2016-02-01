# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autodidact', '0005_auto_20160201_0854'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignment',
            name='locked_until_class_starts',
        ),
        migrations.AddField(
            model_name='assignment',
            name='locked',
            field=models.BooleanField(default=False, help_text=b'Locked assignments will automatically unlock when students register their attendance to class. If registration is disabled, it can only be unlocked by a staff member'),
            preserve_default=True,
        ),
    ]
