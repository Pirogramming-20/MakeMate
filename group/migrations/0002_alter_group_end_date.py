# Generated by Django 4.1 on 2024-02-06 00:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='end_date',
            field=models.DateTimeField(default=datetime.date(2024, 2, 9)),
        ),
    ]
