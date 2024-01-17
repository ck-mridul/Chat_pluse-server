from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail
import uuid


# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length= 255)
    email = models.EmailField(max_length=255, unique=True)
    image = models.ImageField(upload_to='profileImg/',null=True,blank=True)
    username = models.CharField(max_length= 255,null=True,blank=True)
    is_verified = models.BooleanField(default=False)
    token = models.CharField(max_length=250, blank=True, null=True)
    premium = models.BooleanField(default = False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email

@receiver(post_save, sender=User)
def send_verification_email(sender, instance, created, **kwargs):
    
    if created:
        uid = str(uuid.uuid4())
        instance.token = uid
        instance.save()
        print(instance)
        verification_subject = 'Verify Your Account'
        verification_message = 'Please click the link below to verify your account: http://127.0.0.1:3000/verify/{}/'.format(uid)
        send_mail(verification_subject, verification_message, settings.EMAIL_HOST_USER, [instance.email])