# Generated by Django 5.0.1 on 2024-02-11 05:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("group", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="group",
            name="end_date",
            field=models.DateTimeField(default=datetime.date(2024, 2, 14)),
        ),
    ]
