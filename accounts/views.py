from django.contrib.auth import login
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.urls import reverse_lazy
from django.views import generic, View
from django.views.generic import TemplateView
from accounts.forms import UserRegisterForm, MyLoginForm, ProfileRegisterForm, UserUpdateForm
from accounts.helpers import SubscribeOperationsMixin
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


class ProfileSubscribeView(SubscribeOperationsMixin, View):
    def action(self):
        self._subscribe_to_user.followers.add(self._current_profile_user)


class UnsubscribeView(SubscribeOperationsMixin, View):
    def action(self):
        self._current_profile_user.subscribes.remove(self._subscribe_to_user)


class UpdateUser(UserPassesTestMixin, generic.UpdateView):
    model = User
    template_name = 'registration/register.html'
    extra_context = {'title': 'Update'}
    form_class = UserUpdateForm

    def get_context_data(self, **kwargs):
        profile = self.object.profile
        kwargs['profile_form'] = ProfileRegisterForm(instance=profile)
        return super(UpdateUser, self).get_context_data(**kwargs)

    def test_func(self):
        return self.request.user == self.get_object()

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.object.pk})
