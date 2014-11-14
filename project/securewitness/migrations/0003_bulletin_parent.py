# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('securewitness', '0002_auto_20141110_1603'),
    ]

    operations = [
        migrations.AddField(
            model_name='bulletin',
            name='parent',
            field=models.ForeignKey(blank=True, to='securewitness.Bulletin', null=True),
            preserve_default=True,
        ),
    ]
