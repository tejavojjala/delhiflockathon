# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-01 21:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


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
                ('date', models.DateTimeField(auto_now_add=True)),
                ('userName', models.CharField(max_length=100)),
                ('userDp', models.CharField(max_length=1000)),
                ('groupId', models.CharField(max_length=100)),
                ('isPinned', models.BooleanField(default=False)),
                ('text', models.CharField(max_length=2000)),
                ('likes', models.IntegerField(default=0)),
                ('dislikes', models.IntegerField(default=0)),
                ('messageUid', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Reactions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reactorId', models.CharField(max_length=100)),
                ('reactionType', models.CharField(max_length=20)),
                ('foreignKey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pinnedmessages.Messages')),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userToken', models.CharField(max_length=100)),
                ('userId', models.CharField(max_length=100)),
            ],
        ),
    ]
