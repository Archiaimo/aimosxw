# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-12-05 10:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0002_mainnav'),
    ]

    operations = [
        migrations.CreateModel(
            name='MainMustBuy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=64)),
                ('trackid', models.IntegerField(default=1)),
            ],
            options={
                'db_table': 'sxw_mustbuy',
            },
        ),
    ]