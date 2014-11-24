# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('securewitness', '0006_auto_20141113_2113'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='encrypted',
        ),
        migrations.AddField(
            model_name='file',
            name='encryption_key',
            field=models.CharField(default=b'', max_length=32),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bulletin',
            name='description',
            field=models.CharField(max_length=128),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='file',
            name='name',
            field=models.CharField(max_length=128),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='folder',
            name='name',
            field=models.CharField(max_length=128),
            preserve_default=True,
        ),
    ]
