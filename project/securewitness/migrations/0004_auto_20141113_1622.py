# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('securewitness', '0003_bulletin_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bulletin',
            name='location',
            field=models.CharField(default=b'Charlottesville, VA', max_length=200),
            preserve_default=True,
        ),
    ]
