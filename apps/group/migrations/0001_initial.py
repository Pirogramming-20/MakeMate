# Generated by Django 5.0.7 on 2024-07-20 04:16

import datetime
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, verbose_name='그룹 이름')),
                ('password', models.CharField(max_length=15, verbose_name='그룹 비밀번호')),
                ('ability_description1', models.CharField(blank=True, max_length=100, null=True, verbose_name='실력1 설명')),
                ('ability_description2', models.CharField(blank=True, max_length=100, null=True, verbose_name='실력2 설명')),
                ('ability_description3', models.CharField(blank=True, max_length=100, null=True, verbose_name='실력3 설명')),
                ('ability_description4', models.CharField(blank=True, max_length=100, null=True, verbose_name='실력4 설명')),
                ('ability_description5', models.CharField(blank=True, max_length=100, null=True, verbose_name='실력5 설명')),
                ('is_first_end', models.BooleanField(default=False)),
                ('is_second_end', models.BooleanField(default=False)),
                ('is_third_end', models.BooleanField(default=False)),
                ('first_end_date', models.DateTimeField(default=datetime.date(2024, 7, 21))),
                ('second_end_date', models.DateTimeField(default=datetime.date(2024, 7, 22))),
                ('third_end_date', models.DateTimeField(default=datetime.date(2024, 7, 23))),
            ],
        ),
        migrations.CreateModel(
            name='AdminState',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='admin_states', to='group.group')),
            ],
        ),
        migrations.CreateModel(
            name='Idea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=31, null=True, verbose_name='아이디어 이름')),
                ('intro', models.CharField(max_length=50, null=True, verbose_name='아이디어 한 줄 소개')),
                ('file', models.FileField(blank=True, null=True, upload_to='ideas/files/%Y/%m/%d/', verbose_name='첨부파일')),
                ('content', models.TextField(default='기본 설명', max_length=1000, verbose_name='아이디어 설명')),
                ('score', models.IntegerField(default=0, verbose_name='아이디어 점수')),
                ('votes', models.IntegerField(default=0)),
                ('is_selected', models.BooleanField(default=False)),
                ('second_selected', models.BooleanField(default=False)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='idea_member_states', to='group.group')),
                ('member', models.ManyToManyField(blank=True, related_name='idea_member', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MemberState',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_ability', models.PositiveIntegerField(null=True, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)], verbose_name='실력')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='member_states', to='group.group')),
                ('idea_vote1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='idea_vote1_set', to='group.idea')),
                ('idea_vote10', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='idea_vote10_set', to='group.idea')),
                ('idea_vote2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='idea_vote2_set', to='group.idea')),
                ('idea_vote3', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='idea_vote3_set', to='group.idea')),
                ('idea_vote4', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='idea_vote4_set', to='group.idea')),
                ('idea_vote5', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='idea_vote5_set', to='group.idea')),
                ('idea_vote6', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='idea_vote6_set', to='group.idea')),
                ('idea_vote7', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='idea_vote7_set', to='group.idea')),
                ('idea_vote8', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='idea_vote8_set', to='group.idea')),
                ('idea_vote9', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='idea_vote9_set', to='group.idea')),
                ('my_team_idea', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='my_team_idea_set', to='group.idea')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='group.group')),
                ('idea_vote1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vote1_set', to='group.idea')),
                ('idea_vote2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vote2_set', to='group.idea')),
                ('idea_vote3', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vote3_set', to='group.idea')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
