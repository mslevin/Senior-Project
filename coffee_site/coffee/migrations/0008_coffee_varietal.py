# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-29 21:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coffee', '0007_coffee_region'),
    ]

    operations = [
        migrations.AddField(
            model_name='coffee',
            name='varietal',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]