# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-05 07:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coffee', '0023_auto_20160604_2312'),
    ]

    operations = [
        migrations.AddField(
            model_name='brew',
            name='descriptors',
            field=models.CharField(default='', max_length=500),
        ),
    ]
