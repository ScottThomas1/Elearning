# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-23 16:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0016_auto_20180518_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='student_comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.Comment'),
        ),
    ]
