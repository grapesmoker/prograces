# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-09 18:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20170209_1758'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='total_votes',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
