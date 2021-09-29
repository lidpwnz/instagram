from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class Gender(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Profile(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits "
                                         "allowed.")

    avatar = models.ImageField(upload_to=settings.AVATARS_FOLDER)
    info = models.TextField(null=True, blank=True)
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True)
    gender = models.ForeignKey('accounts.Gender', on_delete=models.SET_NULL, null=True)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='profile')
    subscribes = models.ManyToManyField('accounts.Profile', related_name='followers')
