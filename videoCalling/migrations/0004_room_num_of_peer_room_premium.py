# Generated by Django 4.2.7 on 2024-01-02 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videoCalling', '0003_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='num_of_peer',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='room',
            name='premium',
            field=models.BooleanField(default=False),
        ),
    ]