# Generated by Django 5.1.1 on 2024-10-16 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_role',
            field=models.IntegerField(default=0),
        ),
    ]
