# Generated by Django 5.1.3 on 2024-11-09 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Quiz', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='question',
            name='options_count',
            field=models.IntegerField(default=4),
        ),
        migrations.AddField(
            model_name='test',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='test',
            name='questions_count',
            field=models.IntegerField(default=20),
        ),
    ]
