# Generated by Django 4.2.7 on 2024-01-02 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_document_name_document_room_id_document_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='user',
            field=models.JSONField(null=True),
        ),
    ]
