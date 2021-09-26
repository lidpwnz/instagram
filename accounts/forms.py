from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django import forms
from django.core.validators import validate_email
from accounts.models import Profile
from core.helpers import get_widget_attrs


class MyLoginForm(AuthenticationForm):
    def clean(self):
        username_or_email = self.cleaned_data.get('username')

        try:
            validate_email(username_or_email)
            auth_by_email = User.objects.filter(email=username_or_email)
            print(auth_by_email)

            self.cleaned_data['username'] = auth_by_email.first().username

        except (ValidationError, AttributeError) as e:
            print('Exception called. Details:', e)
            auth_by_username = User.objects.filter(username=username_or_email)
            if not auth_by_username.exists():
                raise ValidationError('User with this username/email not found!')

        return super(MyLoginForm, self).clean()


class UserRegisterForm(forms.ModelForm):
    class Meta:
        exclude = []
        model = get_user_model()
        fields = ['username', 'email', 'password', 'first_name', ]
        labels = {'first_name': 'Name'}
        widgets = {
            'username': forms.TextInput(attrs=get_widget_attrs()),
            'email': forms.EmailInput(attrs=get_widget_attrs()),
            'password': forms.PasswordInput(attrs=get_widget_attrs()),
            'first_name': forms.TextInput(attrs=get_widget_attrs()),

        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError('Email is required!')

        users_wth_same_email = User.objects.filter(email=email)
        if users_wth_same_email.exists() and self.instance not in users_wth_same_email:
            raise ValidationError('User with the same email already exists!')
        return email

    def save(self, commit=True):
        user = self.instance
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)

        if commit:
            user.save()
        return user


class ProfileRegisterForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = []
        fields = ['info', 'phone_number', 'gender', 'avatar']
        widgets = {
            'info': forms.Textarea(attrs=get_widget_attrs()),
            'phone_number': forms.TextInput(attrs=get_widget_attrs()),
            'gender': forms.RadioSelect(),
            'avatar': forms.FileInput(attrs=get_widget_attrs())
        }


class UserUpdateForm(UserRegisterForm):
    class Meta(UserRegisterForm.Meta):
        exclude = ['password']
