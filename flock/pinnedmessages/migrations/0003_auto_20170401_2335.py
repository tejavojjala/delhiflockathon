# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-01 23:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pinnedmessages', '0002_comments'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comments',
            old_name='primary_key',
            new_name='primaryKey',
        ),
    ]
