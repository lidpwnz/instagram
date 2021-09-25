from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from accounts.forms import RegisterForm, ProfileForm, MyLoginForm
from accounts.models import Profile


class MyLoginView(LoginView):
    form_class = MyLoginForm

    def form_valid(self, form):
        print('valid')
        print(form.get_user())
        return super(MyLoginView, self).form_valid(form)

    def get_redirect_url(self):
        print(312312312)
        print(self.request.user)
        return reverse_lazy('profile', kwargs={'pk': self.request.user.pk})


class ProfileView(generic.DetailView):
    model = Profile
    template_name = 'user/profile.html'
    context_object_name = 'user_obj'


def test_view(request, *args, **kwargs):
    return render(request, 'registration/register.html', {'form': ProfileForm})


class RegisterView(generic.CreateView):
    model = User
    template_name = 'registration/register.html'
    form_class = RegisterForm
    object = None

    def form_valid(self, form):
        is_email = form.cleaned_data.get('email')
        print(form.cleaned_data)

        if is_email:
            form.instance.email = is_email
        else:
            form.instance.profile.phone_number = form.cleaned_data.get('phone_number')

        form.instance.first_name = form.cleaned_data.get('first_name')
        form.instance.second_name = form.cleaned_data.get('second_name', '')

        self.object = form.save()
        login(self.request, user=self.object)
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.object.pk})
