from django.shortcuts import redirect
from django.urls import reverse_lazy


class MyAuthMiddleware:
    allowed_path = (reverse_lazy('login'), reverse_lazy('register'))
    is_password_reset = None

    def __init__(self, get_response):
        self._get_response = get_response  # View or next middleware

    def __call__(self, request):  # method that calls to take response
        if not request.user.is_authenticated:
            if request.path not in self.allowed_path:
                return redirect('login')

        return self._get_response(request)
