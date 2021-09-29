from django.urls import path
from instagram.views.post_views import (PostCreate,
                                        AddLikeToPostView,
                                        PostDetailView,
                                        PostDeleteView,
                                        FeedView,
                                        AddCommentToPostView,
                                        PostUpdateView
                                        )

urlpatterns = [
    path('', FeedView.as_view(), name='feed'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:post_pk>/detail', PostDetailView.as_view(), name='post_detail'),
    path('<int:post_pk>/update', PostUpdateView.as_view(), name='post_update'),
    path('<int:post_pk>/delete', PostDeleteView.as_view(), name='post_delete'),
    path('<int:post_pk>/add_like', AddLikeToPostView.as_view(), name='add_like'),
    path('<int:post_pk>/add_comment', AddCommentToPostView.as_view(), name='add_comment'),
]
