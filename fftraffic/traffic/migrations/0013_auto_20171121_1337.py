# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-21 13:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('traffic', '0012_auto_20171121_0037'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tablescan',
            name='hands_per_hour',
        ),
        migrations.AlterField(
            model_name='tablescan',
            name='scan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='table_scans', to='traffic.Scan'),
        ),
    ]
