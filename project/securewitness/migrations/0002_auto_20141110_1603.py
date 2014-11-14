# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('securewitness', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bulletin',
            name='encrypted',
        ),
        migrations.AddField(
            model_name='file',
            name='encrypted',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
