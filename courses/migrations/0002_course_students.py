# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-12 12:17
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]