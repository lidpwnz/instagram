from django.urls import path
from instagram.views.post_views import PostCreate, AddLikeToPostView

urlpatterns = [
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:post_pk>/add_like', AddLikeToPostView.as_view(), name='add_like'),
]
