# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-05 05:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rsvp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='invitation',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='rsvp.Invitation'),
            preserve_default=False,
        ),
    ]
