# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-03 08:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0005_auto_20170103_0954'),
    ]

    operations = [
        migrations.AddField(
            model_name='maparea',
            name='title',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
