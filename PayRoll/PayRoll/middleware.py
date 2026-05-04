from django.shortcuts import redirect
from django.conf import settings
from django.urls import resolve

EXEMPT_URLS = [
    'login',  # URL name
    'admin:login',
    'password_reset',
    'password_reset_done',
    'password_reset_confirm',
    'password_reset_complete',
]

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        url_name = resolve(request.path_info).url_name

        if not request.user.is_authenticated and url_name not in EXEMPT_URLS:
            return redirect('login')

        return self.get_response(request)
