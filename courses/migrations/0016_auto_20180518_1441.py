# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-18 18:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0015_auto_20180518_1055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='student_comment',
            field=models.TextField(blank=True),
        ),
    ]
