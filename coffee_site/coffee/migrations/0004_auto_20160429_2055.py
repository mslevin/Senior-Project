# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-29 20:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coffee', '0003_auto_20160426_0050'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coffee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200)),
                ('tasting_notes', models.CharField(max_length=500)),
                ('roast_date', models.DateField()),
                ('brew_date', models.DateField()),
                ('test_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Roaster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
                ('website', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='coffee',
            name='roaster',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coffee.Roaster'),
        ),
    ]
