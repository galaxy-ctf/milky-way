# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-05-20 23:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('milkyway', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
