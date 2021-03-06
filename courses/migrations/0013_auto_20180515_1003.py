# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-15 14:03
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0012_section_public_students'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='section',
            name='public_students',
        ),
        migrations.AddField(
            model_name='course',
            name='public_students',
            field=models.ManyToManyField(related_name='public_courses', to=settings.AUTH_USER_MODEL),
        ),
    ]
