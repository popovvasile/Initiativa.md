# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-07-25 12:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0003_auto_20160716_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='law',
            name='question',
            field=models.CharField(default='', max_length=400),
        ),
    ]
