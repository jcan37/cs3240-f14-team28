# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('securewitness', '0008_auto_20141119_0358'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='permission',
            name='file',
        ),
        migrations.AddField(
            model_name='bulletin',
            name='encrypted',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='permission',
            name='bulletin',
            field=models.ForeignKey(default=None, to='securewitness.Bulletin'),
            preserve_default=False,
        ),
    ]
