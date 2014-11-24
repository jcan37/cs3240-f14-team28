# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('securewitness', '0011_auto_20141123_2031'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='content_type',
            field=models.CharField(default=b'', max_length=128),
            preserve_default=True,
        ),
    ]
