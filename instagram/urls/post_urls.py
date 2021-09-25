from django.urls import path
from instagram.views.post_views import PostCreate

urlpatterns = [
    path('create/', PostCreate.as_view(), name='post_create'),
]
