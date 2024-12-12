# Generated by Django 3.2.25 on 2024-12-11 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0009_question_question_banks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='type',
            field=models.CharField(choices=[('单项选择题', '单项选择题'), ('多项选择题', '多项选择题'), ('判断题', '判断题'), ('填空题', '填空题'), ('解答题', '解答题')], max_length=20),
        ),
    ]
