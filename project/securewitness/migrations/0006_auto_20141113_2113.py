# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('securewitness', '0005_auto_20141113_2045'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='url',
        ),
        migrations.AddField(
            model_name='file',
            name='name',
            field=models.CharField(default=datetime.datetime(2014, 11, 14, 2, 13, 1, 635614, tzinfo=utc), max_length=256),
            preserve_default=False,
        ),
    ]
