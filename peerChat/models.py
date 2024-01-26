from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

# Create your models here.

class ThreadManager(models.Manager):
    def by_user(self, **kwargs):
        user = kwargs.get('user')
        lookup = Q(first_person=user) | Q(second_person=user)
        qs = self.get_queryset().filter(lookup).distinct()
        return qs


class Thread(models.Model):
    first_person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='thread_first_person')
    second_person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                                     related_name='thread_second_person')
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    block_by = models.BigIntegerField(null=True, blank=True,)
    hide_by_frst = models.BooleanField(default = False)
    hide_by_second = models.BooleanField(default = False)

    objects = ThreadManager()
    class Meta:
        unique_together = ['first_person', 'second_person']


class Media(models.Model):
    media = models.FileField(upload_to='chat/media',null=True, blank=True)
    media_type = models.CharField(max_length=50,null=True, blank=True)

class ChatMessage(models.Model):
    thread = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.CASCADE, related_name='chatmessage_thread')
    userId = models.BigIntegerField()
    message = models.TextField()
    media = models.ForeignKey(Media,on_delete = models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)