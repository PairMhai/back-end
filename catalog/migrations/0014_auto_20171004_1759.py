# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-04 10:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0013_merge_20171004_0103'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='product',
            name='updated_at',
        ),
        migrations.AlterField(
            model_name='product',
            name='design',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.Design'),
        ),
        migrations.AlterField(
            model_name='product',
            name='material',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.Material'),
        ),
    ]
