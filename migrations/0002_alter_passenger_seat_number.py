# Generated by Django 5.0.9 on 2024-12-26 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airline_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passenger',
            name='seat_number',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
