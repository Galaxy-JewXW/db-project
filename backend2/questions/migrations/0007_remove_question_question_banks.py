# Generated by Django 3.2.25 on 2024-11-28 16:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0006_question_option_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='question_banks',
        ),
    ]
