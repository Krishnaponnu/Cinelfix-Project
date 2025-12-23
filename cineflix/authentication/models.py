from django.db import models

from movies.models import BaseClass

from django.contrib.auth.models import AbstractUser

# Create your models here.

class RoleChoices(models.TextChoices):

    USER = 'User','User'

    ADMIN = 'Admin','Admin'

class Profile(AbstractUser):

    role = models.CharField(max_length=10,choices=RoleChoices.choices)

    phone = models.CharField(null=True,blank=True)

    phone_verified = models.BooleanField(default=False)

    class Meta:
        
        verbose_name = 'Profiles'

        verbose_name_plural = 'Profiles'
         
    def __str__(self):
         
        return f'{self.username}'
    
class OTP(BaseClass):

    profile = models.OneToOneField('Profile',on_delete=models.CASCADE)

    otp = models.CharField(max_length=4)

    email_otp = models.CharField(max_length=4)

    email_otp_verified = models.BooleanField(default=False)
    class Meta:
        
        verbose_name = 'OTPs'

        verbose_name_plural = 'OTPs'
         
    def __str__(self):
         
        return f'{self.username}otp'