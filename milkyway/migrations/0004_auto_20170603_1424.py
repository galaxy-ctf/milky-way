# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-06-03 14:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
        ('milkyway', '0003_challenge_lesson'),
    ]

    operations = [
        migrations.AddField(
            model_name='hint',
            name='show',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterUniqueTogether(
            name='solves',
            unique_together=set([('challenge', 'team')]),
        ),
    ]
