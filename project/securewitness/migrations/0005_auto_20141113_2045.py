# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('securewitness', '0004_auto_20141113_1622'),
    ]

    operations = [
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='bulletin',
            name='description',
            field=models.CharField(max_length=512),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bulletin',
            name='location',
            field=models.CharField(default=b'Charlottesville, VA', max_length=256),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bulletin',
            name='parent',
            field=models.ForeignKey(blank=True, to='securewitness.Folder', null=True),
            preserve_default=True,
        ),
    ]
