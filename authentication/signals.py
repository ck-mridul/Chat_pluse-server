# # from django.db.models.signals import post_save
# # from django.dispatch import receiver
# # from django.core.mail import send_mail
# # from .models import User
# # from django.conf import settings
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import User

# @receiver(post_save, sender=User)
# def send_verification_email(sender, instance, **kwargs):
#     print('h')
#     print('sender:',sender,'instance:',instance,'kwargs :',kwargs)