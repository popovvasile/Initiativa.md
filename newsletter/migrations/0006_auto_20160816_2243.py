# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-08-16 22:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0005_auto_20160727_1101'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='news',
            options={'verbose_name': 'New'},
        ),
        migrations.RemoveField(
            model_name='law',
            name='news_website',
        ),
    ]