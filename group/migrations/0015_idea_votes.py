# Generated by Django 4.2.9 on 2024-02-05 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0014_alter_group_end_date_vote'),
    ]

    operations = [
        migrations.AddField(
            model_name='idea',
            name='votes',
            field=models.IntegerField(default=0),
        ),
    ]
