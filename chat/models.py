from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Create your models here.

class Document(models.Model):
    room_id = models.CharField(max_length = 10)
    name = models.CharField(max_length = 100)
    pdf = models.FileField(upload_to='documents')
    size = models.FloatField()
    user_name = models.CharField(max_length = 100)
    user_id = models.BigIntegerField()
    
    def __str__(self):
        return self.name
    
    
@receiver(post_save, sender=Document)
def document_signal(sender, instance, created, **kwargs):
    print('signal')
    
    if created:
        channel_layer = get_channel_layer()
        room_id = instance.room_id
        print(room_id)
        
        async_to_sync(channel_layer.group_send)(
            f"document-{room_id}", {
                'type': 'send_doc',
                'document': 'all'
            }
        )
        