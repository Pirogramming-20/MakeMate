# Generated by Django 4.2.9 on 2024-02-17 08:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0002_remove_group_choice_remove_group_team_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='end_date',
            field=models.DateTimeField(default=datetime.date(2024, 2, 20)),
        ),
    ]
