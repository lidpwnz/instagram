from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django import forms
from django.db.models import Q
from django.core.validators import validate_email
from accounts.models import Profile
from core.helpers import get_widget_attrs


class MyLoginForm(AuthenticationForm):
    def clean(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if not User.objects.get(username=username) and not User.objects.get(email=email):
            raise ValidationError('User not found!')

        return super(MyLoginForm, self).clean()


class RegisterForm(forms.ModelForm):
    phone_or_email = forms.CharField(max_length=70, widget=forms.TextInput(attrs=get_widget_attrs()))
    fullname = forms.CharField(max_length=150, widget=forms.TextInput(attrs=get_widget_attrs()))

    class Meta:
        model = get_user_model()
        fields = ['phone_or_email', 'fullname', 'username', 'password']
        widgets = {
            'username': forms.TextInput(attrs=get_widget_attrs()),
            'password': forms.PasswordInput(attrs=get_widget_attrs())
        }

    def clean_phone_or_email(self):
        user_input = self.cleaned_data.get('phone_or_email')
        try:
            validate_email(user_input)
            self.cleaned_data['email'] = user_input
        except Exception as e:
            print('Exception details:', e)

        if user_input.lstrip('+').isdigit():
            self.cleaned_data['phone_number'] = user_input

        return user_input

    def save(self, commit=True):
        user = self.instance
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    def clean_fullname(self):
        fullname = self.cleaned_data.get('fullname').split()

        context = {}
        if len(fullname) > 1:
            context['first_name'], context['last_name'] = fullname
        else:
            context['first_name'] = fullname[0]

        self.cleaned_data.update(context)
        return fullname

    def clean(self):
        phone_or_email = self.cleaned_data.get('phone_or_email')
        if phone_or_email and User.objects.filter(Q(email=phone_or_email) | Q(profile__phone_number=phone_or_email)):
            raise ValidationError('User with this email/phone already exists!')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'

