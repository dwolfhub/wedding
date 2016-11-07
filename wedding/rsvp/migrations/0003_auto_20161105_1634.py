# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-05 16:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rsvp', '0002_person_invitation'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='person',
            options={'verbose_name_plural': 'people'},
        ),
        migrations.AddField(
            model_name='person',
            name='coming',
            field=models.BooleanField(default=False),
        ),
    ]