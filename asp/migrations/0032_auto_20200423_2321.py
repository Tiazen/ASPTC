# Generated by Django 2.1.5 on 2020-04-23 20:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asp', '0031_auto_20200423_2108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solution',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 23, 23, 21, 19, 149584)),
        ),
        migrations.AlterField(
            model_name='theme',
            name='theme',
            field=models.CharField(max_length=1000, unique=True),
        ),
    ]