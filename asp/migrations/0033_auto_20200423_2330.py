# Generated by Django 2.1.5 on 2020-04-23 20:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asp', '0032_auto_20200423_2321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solution',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 23, 23, 30, 14, 190242)),
        ),
        migrations.AlterField(
            model_name='theme',
            name='theme',
            field=models.CharField(max_length=1000),
        ),
    ]