# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-07-16 18:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='law',
            name='posted',
            field=models.BooleanField(default=False, verbose_name='Posteaza'),
        ),
    ]