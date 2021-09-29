from abc import abstractmethod
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from accounts.models import Profile


class SubscribeOperationsMixin(View):
    _current_profile_user = None
    _subscribe_to_user = None

    def dispatch(self, request, *args, **kwargs):
        self._current_profile_user = self.request.user.profile
        self._subscribe_to_user = get_object_or_404(Profile, pk=kwargs.get('pk'))
        if self._current_profile_user == self._subscribe_to_user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    @abstractmethod
    def action(self):
        raise NotImplementedError

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.kwargs.get('pk')})

    def post(self, request, *args, **kwargs):
        self.action()
        return redirect(self.get_success_url())