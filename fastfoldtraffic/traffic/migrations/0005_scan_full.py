# Generated by Django 2.0.2 on 2018-03-07 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('traffic', '0004_scan_start_datetime'),
    ]

    operations = [
        migrations.AddField(
            model_name='scan',
            name='full',
            field=models.BooleanField(default=True),
        ),
    ]
