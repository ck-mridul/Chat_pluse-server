# Generated by Django 4.2.7 on 2024-01-02 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_rename_is_verifyed_user_is_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='premium',
            field=models.BooleanField(default=False),
        ),
    ]
