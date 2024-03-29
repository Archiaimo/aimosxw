# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-12-07 14:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0010_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('o_price', models.FloatField(default=0)),
                ('o_time', models.DateTimeField(auto_now=True)),
                ('o_status', models.IntegerField(default=1)),
                ('o_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.User')),
            ],
            options={
                'db_table': 'sxw_order',
            },
        ),
        migrations.CreateModel(
            name='OrderGoods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('o_goods_num', models.IntegerField(default=1)),
                ('o_goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.Goods')),
                ('o_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.Order')),
            ],
            options={
                'db_table': 'sxw_ordergoods',
            },
        ),
    ]
