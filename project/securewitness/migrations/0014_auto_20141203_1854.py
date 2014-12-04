# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('securewitness', '0013_folder_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='Filing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bulletin', models.ForeignKey(to='securewitness.Bulletin')),
                ('folder', models.ForeignKey(to='securewitness.Folder')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='bulletin',
            name='parent',
        ),
        migrations.AlterField(
            model_name='bulletin',
            name='location',
            field=models.CharField(default=b'Charlottesville, VA', max_length=128),
            preserve_default=True,
        ),
    ]
