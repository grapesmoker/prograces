# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-09 17:58
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20170209_1745'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='district',
            name='geometry',
        ),
        migrations.AddField(
            model_name='district',
            name='mp_geometry',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=4326),
        ),
        migrations.AddField(
            model_name='district',
            name='p_geometry',
            field=django.contrib.gis.db.models.fields.PolygonField(null=True, srid=4326),
        ),
    ]
