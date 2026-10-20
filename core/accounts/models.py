from django.db import models
from django.contrib.auth.models  import AbstractUser
from .manager import UserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
import uuid
from django.conf import settings

# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10, blank=True, default="")
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, null=True, blank=True)
    email_verification_token = models.CharField(max_length=200, null=True, blank=True)
    forgot_password_token = models.CharField(max_length=200, null=True, blank=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def name(self):
        return self.first_name + " " + self.last_name

    def __str__(self):
        return self.email


@receiver(post_save, sender=User)
def send_email_token(sender, instance, created, **kwargs):
    if created:
        try:
            subject = 'To verify your email account'
            message = f'Hi, this email is to verify your email account, just click on the link to verify http://127.0.0.1:8000/{uuid.uuid4()}/'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [instance.email]
            send_mail(subject, message, email_from, recipient_list)
        except Exception as e:
            print(e)


