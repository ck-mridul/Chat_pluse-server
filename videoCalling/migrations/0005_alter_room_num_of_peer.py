# Generated by Django 4.2.7 on 2024-01-12 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videoCalling', '0004_room_num_of_peer_room_premium'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='num_of_peer',
            field=models.BigIntegerField(default=1),
        ),
    ]
