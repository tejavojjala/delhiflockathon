# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-01 15:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('primaryKey', models.AutoField(primary_key=True, serialize=False)),
                ('userId', models.CharField(max_length=100)),
                ('userName', models.CharField(max_length=100)),
                ('userDp', models.CharField(max_length=1000)),
                ('groupId', models.CharField(max_length=100)),
                ('isPinned', models.BooleanField(default=False)),
                ('text', models.CharField(max_length=2000)),
                ('likes', models.IntegerField(default=0)),
                ('dislikes', models.IntegerField(default=0)),
            ],
        ),
    ]
