from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class Gender(models.Model):
    name = models.CharField(max_length=50)


class Profile(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

    avatar = models.ImageField(upload_to=settings.AVATARS_FOLDER, default=settings.AVATARS_DEFAULT)
    info = models.TextField(null=True, blank=True)
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True)
    gender = models.ForeignKey('accounts.Gender', on_delete=models.SET_NULL, null=True)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='profile')

    posts_count = models.IntegerField(default=0)
    subscribes_count = models.IntegerField(default=0)
    followers_count = models.IntegerField(default=0)


class Subscribes(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='followers')
    follower = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='subscribes')
