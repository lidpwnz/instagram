from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views import generic
from accounts.forms import UserRegisterForm, MyLoginForm, ProfileRegisterForm
from accounts.models import Profile


class MyLoginView(LoginView):
    form_class = MyLoginForm

    def get_redirect_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.request.user.pk})


class ProfileView(generic.DetailView):
    model = Profile
    template_name = 'user/profile.html'
    context_object_name = 'profile'


class RegisterView(generic.CreateView):
    model = User
    template_name = 'registration/register.html'
    form_class = UserRegisterForm
    profile_form = ProfileRegisterForm
    object = None

    def get_context_data(self, **kwargs):
        kwargs['profile_form'] = self.profile_form()
        return super(RegisterView, self).get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        profile_form = self.profile_form(data=request.POST, files=request.FILES)
        form = self.get_form()
        if form.is_valid() and profile_form.is_valid():
            return self.my_form_valid(form, profile_form)
        else:
            return self.my_form_invalid(form, profile_form)

    def my_form_invalid(self, form, profile_form):
        context = {'form': form, 'profile_form': profile_form}
        return self.render_to_response(context=context)

    def my_form_valid(self, form, profile_form):
        response = super().form_valid(form)
        profile_form.instance.user = self.object
        profile_form.save()

        login(self.request, user=self.object)
        return response

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.object.pk})
