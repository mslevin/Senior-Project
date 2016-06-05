# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-05 06:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('coffee', '0022_userdata_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='secondaryflavor',
            name='parent_flavor',
        ),
        migrations.RemoveField(
            model_name='tertiaryflavor',
            name='parent_flavor',
        ),
        migrations.AlterField(
            model_name='brew',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='time',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True),
        ),
        migrations.DeleteModel(
            name='PrimaryFlavor',
        ),
        migrations.DeleteModel(
            name='SecondaryFlavor',
        ),
        migrations.DeleteModel(
            name='TertiaryFlavor',
        ),
    ]