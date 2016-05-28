# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-19 02:12
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('coffee', '0005_auto_20160518_1906'),
    ]

    operations = [
        migrations.AddField(
            model_name='brew',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='brew',
            name='date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]