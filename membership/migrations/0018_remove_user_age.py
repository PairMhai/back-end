# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-28 16:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0017_merge_20170928_1339'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='age',
        ),
    ]
