# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-07-21 11:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0004_teacher_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='birday',
            field=models.DateField(blank=True, null=True, verbose_name='\u751f\u65e5'),
        ),
    ]