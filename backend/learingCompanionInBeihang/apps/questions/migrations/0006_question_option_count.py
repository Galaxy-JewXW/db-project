# Generated by Django 5.1.1 on 2024-11-23 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0005_alter_question_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='option_count',
            field=models.IntegerField(default=0),
        ),
    ]
