# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-28 18:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_auto_20170928_0948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creditcard',
            name='expire_date',
            field=models.DateField(),
        ),
    ]
