# Generated by Django 4.2.1 on 2023-05-25 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NYRABias', '0006_alter_race_fieldsize'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='race',
            constraint=models.UniqueConstraint(fields=('date', 'track', 'raceNumber'), name='unique_race'),
        ),
    ]
