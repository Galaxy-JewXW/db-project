# Generated by Django 5.1.1 on 2024-11-20 16:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0003_blacklist'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionBank',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('subject', models.CharField(max_length=100)),
                ('estimated_time', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('question_count', models.IntegerField(default=0)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_question_banks', to='users.user')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('单项选择题', '单项选择题'), ('多项选择题', '多项选择题'), ('填空题', '填空题'), ('问答题', '问答题')], max_length=20)),
                ('content', models.TextField()),
                ('subject', models.CharField(max_length=100)),
                ('added_at', models.DateField()),
                ('source', models.CharField(blank=True, max_length=100, null=True)),
                ('tags', models.JSONField()),
                ('difficulty', models.CharField(choices=[('简单', '简单'), ('中等', '中等'), ('困难', '困难')], max_length=10)),
                ('answer', models.TextField(blank=True, null=True)),
                ('added_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='added_questions', to='users.user')),
                ('question_banks', models.ManyToManyField(related_name='questions', to='questions.questionbank')),
            ],
        ),
        migrations.CreateModel(
            name='UserQuestionRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_correct', models.BooleanField()),
                ('attempted_at', models.DateTimeField(auto_now_add=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_records', to='questions.question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_records', to='users.user')),
            ],
            options={
                'verbose_name': '用户做题记录',
                'verbose_name_plural': '用户做题记录',
                'unique_together': {('user', 'question')},
            },
        ),
    ]
