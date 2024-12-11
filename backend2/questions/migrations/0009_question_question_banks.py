# Generated by Django 3.2.25 on 2024-12-09 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0008_questionbank_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='question_banks',
            field=models.ManyToManyField(related_name='questions', to='questions.QuestionBank'),
        ),
    ]
