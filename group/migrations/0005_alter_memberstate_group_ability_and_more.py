# Generated by Django 4.1 on 2024-02-01 06:18

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0004_idea_memberstate_adminstate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memberstate',
            name='group_ability',
            field=models.PositiveIntegerField(null=True, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)], verbose_name='실력'),
        ),
        migrations.AlterField(
            model_name='memberstate',
            name='group_tech_stack',
            field=models.CharField(choices=[('PM', '기획'), ('DESIGN', '디자인'), ('FE', '프론트엔드'), ('BE', '백엔드'), ('SERVER', '배포/서버')], max_length=10, null=True, verbose_name='기술 스택'),
        ),
        migrations.AlterField(
            model_name='memberstate',
            name='idea_vote1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='idea_vote1_set', to='group.idea'),
        ),
        migrations.AlterField(
            model_name='memberstate',
            name='idea_vote2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='idea_vote2_set', to='group.idea'),
        ),
        migrations.AlterField(
            model_name='memberstate',
            name='idea_vote3',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='idea_vote3_set', to='group.idea'),
        ),
    ]