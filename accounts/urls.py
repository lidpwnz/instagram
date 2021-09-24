from django.urls import path, include
from django.contrib.auth import views
from accounts.forms import MyLoginForm


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('login/', views.LoginView.as_view(form_class=MyLoginForm), name='login'),


]
