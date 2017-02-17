# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-17 08:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('readers', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=128, unique=True)),
                ('title', models.CharField(max_length=128)),
                ('author', models.CharField(max_length=128)),
                ('year', models.IntegerField()),
                ('language', models.CharField(max_length=64)),
                ('is_available', models.BooleanField(default=True)),
                ('reader', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='readers.Reader')),
            ],
        ),
    ]
