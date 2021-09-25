from django.urls import path, include
from accounts.views import ProfileView, RegisterView, test_view, MyLoginView
from django.contrib.auth import views


urlpatterns = [
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    # path('', include('django.contrib.auth.urls')),
    path('<int:pk>/profile/', ProfileView.as_view(), name='profile'),
    path('register/', RegisterView.as_view(), name='register'),
    path('test/', test_view)

]
