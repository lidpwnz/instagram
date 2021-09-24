from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def get_widget_attrs(**kwargs):
    context = {'class': 'form-control mb-3'}
    if kwargs:
        context.update(kwargs)
    return context


class MyLoginForm(AuthenticationForm):
    def clean(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if not User.objects.get(username=username) and not User.objects.get(email=email):
            raise ValidationError('User not found!')


