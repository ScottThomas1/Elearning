# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-26 17:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0009_auto_20180417_1153'),
    ]

    operations = [
        migrations.AddField(
            model_name='useranswer',
            name='time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
