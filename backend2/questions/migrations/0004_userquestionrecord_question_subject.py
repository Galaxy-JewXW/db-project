# Generated by Django 5.1.1 on 2024-11-21 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0003_alter_question_subject_alter_questionbank_subject_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userquestionrecord',
            name='question_subject',
            field=models.CharField(choices=[('工科数学分析（上）', '工科数学分析（上）'), ('工科数学分析（下）', '工科数学分析（下）'), ('工科高等代数', '工科高等代数'), ('离散数学（信息类）', '离散数学（信息类）'), ('基础物理学A', '基础物理学A')], default='工科数学分析（上）', max_length=100),
        ),
    ]