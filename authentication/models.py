from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length= 255)
    email = models.EmailField(max_length=255, unique=True)
    image = models.ImageField(upload_to='profileImg/',null=True,blank=True)
    username = models.CharField(max_length= 255,null=True,blank=True)
    is_verifyed = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email

@receiver(post_save, sender=User)
def post_save_receiver(sender,instance, **kwargs):
    print('user crated!')
    print(sender,instance,kwargs)

