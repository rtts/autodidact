# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import adminsortable.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('autodidact', '0003_auto_20160130_0030'),
    ]

    operations = [
        migrations.RenameModel('Activity', 'Step'),
        migrations.RenameModel('CompletedActivity', 'CompletedStep'),
        migrations.RenameModel('Group', 'Class'),
    ]
