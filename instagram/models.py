from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings


class Post(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='posts')
    img = models.ImageField(upload_to=settings.POST_PICS_FOLDER)
    description = models.TextField()
    likes_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.owner} | likes: {self.likes_count} | comments: {self.comments_count}'


class Like(models.Model):
    post = models.ForeignKey('instagram.Post', on_delete=models.CASCADE, related_name='users_who_like_it')
    liked_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        return f'{self.post} | liker: {self.liked_user}'

