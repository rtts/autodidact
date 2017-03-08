# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autodidact', '0005_auto_20170308_1145'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='programme',
            options={'ordering': ['order']},
        ),
    ]
