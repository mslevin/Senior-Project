# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-05 04:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coffee', '0018_auto_20160603_1457'),
    ]

    operations = [
        migrations.RenameField(
            model_name='brew',
            old_name='initial_score',
            new_name='overall_score',
        ),
        migrations.AddField(
            model_name='brew',
            name='acidity',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='brew',
            name='aftertaste',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='brew',
            name='body',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='brew',
            name='extraction',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='brew',
            name='strength',
            field=models.IntegerField(default=-1),
        ),
    ]
