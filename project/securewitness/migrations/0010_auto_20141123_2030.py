# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('securewitness', '0009_auto_20141123_2028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permission',
            name='bulletin',
            field=models.ForeignKey(to='securewitness.Bulletin', null=True),
            preserve_default=True,
        ),
    ]
