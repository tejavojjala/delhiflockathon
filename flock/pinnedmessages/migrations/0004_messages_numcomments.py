# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-02 02:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pinnedmessages', '0003_auto_20170401_2335'),
    ]

    operations = [
        migrations.AddField(
            model_name='messages',
            name='numcomments',
            field=models.IntegerField(default=0),
        ),
    ]
