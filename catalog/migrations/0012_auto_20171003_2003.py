# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-03 13:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0011_auto_20170928_0924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='design',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='catalog.Design'),
        ),
    ]
