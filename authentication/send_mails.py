from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

# @shared_task
# change celery to normal due to hosting on rendor
def send_verification_email(email,uid):
    verification_subject = 'Verify Your Account'
    verification_message = 'Please click the link below to verify your account: https://chat-pulse.vercel.app/verify/{}/'.format(uid)
    send_mail(verification_subject, verification_message, settings.EMAIL_HOST_USER, [email])
