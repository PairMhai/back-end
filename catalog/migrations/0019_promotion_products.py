# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-22 15:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0018_merge_20171022_1608'),
    ]

    operations = [
        migrations.AddField(
            model_name='promotion',
            name='products',
            field=models.ManyToManyField(to='catalog.Product'),
        ),
    ]