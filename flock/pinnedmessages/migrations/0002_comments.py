# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-01 23:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pinnedmessages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('primary_key', models.AutoField(primary_key=True, serialize=False)),
                ('userId', models.CharField(max_length=100)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('userName', models.CharField(max_length=100)),
                ('userDp', models.CharField(max_length=1000)),
                ('text', models.CharField(max_length=2000)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pinnedmessages.Messages')),
            ],
        ),
    ]