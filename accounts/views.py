from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic, View
from django.views.generic import TemplateView

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


class SearchView(TemplateView):
    template_name = 'user/list.html'

    def get_search_params(self):
        return self.request.GET.get('params')

    def get_users(self):
        params = self.get_search_params()
        username_ = Q(username__icontains=params)
        email_ = Q(email__icontains=params)
        first_name_ = Q(first_name__icontains=params)

        return User.objects.filter(username_ | email_ | first_name_)

    def get_context_data(self, **kwargs):
        return super(SearchView, self).get_context_data(users=self.get_users())


class ProfileSubscribeView(View):

    def dispatch(self, request, *args, **kwargs):
        current_profile_user = self.request.user.profile
        subscribe_to_user = get_object_or_404(Profile, pk=kwargs.get('pk'))
        if current_profile_user in subscribe_to_user.followers.all():
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        current_profile = self.request.user.profile
        subscribe_to_user = get_object_or_404(Profile, pk=kwargs.get('pk'))
        subscribe_to_user.followers.add(current_profile)
        return redirect('profile', pk=kwargs.get('pk'))


class UnsubscribeView(View):
    def get(self, request, *args, **kwargs):
        current_profile = self.request.user.profile
        subscribe_to_profile = get_object_or_404(Profile, pk=kwargs.get('pk'))
        print(current_profile.followers.all())
        current_profile.subscribes.remove(subscribe_to_profile)
        print(subscribe_to_profile.subscribes.all())
        return redirect('profile', pk=subscribe_to_profile.pk)
