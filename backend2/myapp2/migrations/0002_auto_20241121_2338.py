# Generated by Django 3.2.25 on 2024-11-21 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp2', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='college',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='entry_year',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='role',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
