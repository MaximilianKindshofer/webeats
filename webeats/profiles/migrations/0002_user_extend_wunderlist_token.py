# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-22 19:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_extend',
            name='wunderlist_token',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
