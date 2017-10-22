# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-21 18:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0016_auto_20171021_2139'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='promotion',
            name='description',
        ),
        migrations.AddField(
            model_name='promotion',
            name='end_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='promotion',
            name='start_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='design',
            name='yard',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
        ),
    ]
