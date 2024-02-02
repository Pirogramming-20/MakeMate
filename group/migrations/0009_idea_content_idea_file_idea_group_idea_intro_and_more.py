# Generated by Django 4.2.9 on 2024-02-02 12:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0008_alter_adminstate_group_alter_memberstate_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='idea',
            name='content',
            field=models.TextField(default=1, verbose_name='내용'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='idea',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='ideas/files/%Y/%m/%d/', verbose_name='첨부파일'),
        ),
        migrations.AddField(
            model_name='idea',
            name='group',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='ideas', to='group.group'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='idea',
            name='intro',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='한 줄 소개'),
        ),
        migrations.AlterField(
            model_name='idea',
            name='title',
            field=models.CharField(max_length=100, verbose_name='아이디어 이름'),
        ),
    ]