from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class Gender(models.Model):
    name = models.CharField(max_length=50)


class Profile(models.Model):
    avatar = models.ImageField(upload_to=settings.AVATARS_FOLDER, default=settings.AVATARS_DEFAULT)
    info = models.TextField(null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True, unique=True)
    gender = models.ForeignKey('accounts.Gender', on_delete=models.SET_NULL, null=True)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)

    posts_count = models.IntegerField(default=0)
    subscribes_count = models.IntegerField(default=0)
    followers_count = models.IntegerField(default=0)


class Subscribes(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='followers')
    follower = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='subscribes')
