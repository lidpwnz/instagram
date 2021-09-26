from django.contrib.auth import get_user_model
from django.db import models


class Post(models.Model):
    owner = models.ForeignKey(get_user_model(), related_name='posts', on_delete=models.CASCADE)
    img = models.ImageField(upload_to='post_pics', null=False, blank=False)
    description = models.TextField(max_length=2200, null=False, blank=False)
    likes_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.owner} | likes: {self.likes_count} | comments: {self.comments_count}'


class Like(models.Model):
    post = models.ForeignKey('instagram.Post', on_delete=models.CASCADE, related_name='users_who_like_it')
    liked_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        return f'{self.post} | liker: {self.liked_user}'

