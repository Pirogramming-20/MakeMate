# Generated by Django 4.2.9 on 2024-02-02 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0006_merge_20240202_1627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='ability_description1',
            field=models.CharField(max_length=100, null=True, verbose_name='실력1 설명'),
        ),
        migrations.AlterField(
            model_name='group',
            name='ability_description2',
            field=models.CharField(max_length=100, null=True, verbose_name='실력2 설명'),
        ),
        migrations.AlterField(
            model_name='group',
            name='ability_description3',
            field=models.CharField(max_length=100, null=True, verbose_name='실력3 설명'),
        ),
        migrations.AlterField(
            model_name='group',
            name='ability_description4',
            field=models.CharField(max_length=100, null=True, verbose_name='실력4 설명'),
        ),
        migrations.AlterField(
            model_name='group',
            name='ability_description5',
            field=models.CharField(max_length=100, null=True, verbose_name='실력5 설명'),
        ),
        migrations.AlterField(
            model_name='group',
            name='choice',
            field=models.IntegerField(default=3, null=True, verbose_name='그룹 최대 투표 개수'),
        ),
        migrations.AlterField(
            model_name='group',
            name='type',
            field=models.CharField(choices=[('모각코', '모각코'), ('프로젝트', '프로젝트')], max_length=20, verbose_name='모임 종류'),
        ),
    ]