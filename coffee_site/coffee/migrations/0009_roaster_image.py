# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-29 22:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coffee', '0008_coffee_varietal'),
    ]

    operations = [
        migrations.AddField(
            model_name='roaster',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=b''),
        ),
    ]