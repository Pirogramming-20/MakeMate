# Generated by Django 4.1 on 2024-02-01 03:34

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('group', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='type',
            field=models.CharField(choices=[('모각코', '모각코'), ('프로젝트', '프로젝트')], default=1, max_length=20, verbose_name='모임 종류'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='group',
            name='ability_description1',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='실력1 설명'),
        ),
        migrations.AlterField(
            model_name='group',
            name='ability_description2',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='실력2 설명'),
        ),
        migrations.AlterField(
            model_name='group',
            name='ability_description3',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='실력3 설명'),
        ),
        migrations.AlterField(
            model_name='group',
            name='ability_description4',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='실력4 설명'),
        ),
        migrations.AlterField(
            model_name='group',
            name='ability_description5',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='실력5 설명'),
        ),
        migrations.AlterField(
            model_name='group',
            name='choice',
            field=models.IntegerField(blank=True, default=3, null=True, verbose_name='그룹 최대 투표 개수'),
        ),
        migrations.AlterField(
            model_name='group',
            name='team_building',
            field=models.ManyToManyField(null=True, related_name='user_groups', to=settings.AUTH_USER_MODEL),
        ),
    ]