from django.urls import path, include
from accounts.views import ProfileView, RegisterView, MyLoginView, ProfileSubscribeView, UnsubscribeView, UpdateUser
from django.contrib.auth import views


urlpatterns = [
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('', include('django.contrib.auth.urls')),
    path('<int:pk>/profile/', ProfileView.as_view(), name='profile'),
    path('register/', RegisterView.as_view(), name='register'),
    path('<int:pk>/profile/subscribe', ProfileSubscribeView.as_view(), name='subscribe'),
    path('<int:pk>/profile/unsubscribe', UnsubscribeView.as_view(), name='unsubscribe'),
    path('<int:pk>/update', UpdateUser.as_view(), name='update_user')
]
