# Generated by Django 5.1.1 on 2024-11-22 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('broadcast', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='broadcast',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='broadcast',
            name='title',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
