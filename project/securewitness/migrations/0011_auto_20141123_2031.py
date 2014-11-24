# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('securewitness', '0010_auto_20141123_2030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permission',
            name='bulletin',
            field=models.ForeignKey(default=1, to='securewitness.Bulletin'),
            preserve_default=False,
        ),
    ]
