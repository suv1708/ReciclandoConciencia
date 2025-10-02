# users/middleware.py
from django.shortcuts import redirect
from django.urls import reverse


class ProfileCompletionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # chequear que tenga los campos obligatorios
            if (not request.user.phone or not request.user.birth_date or not request.user.photo):
                allowed_urls = [
                    reverse("complete_profile"),
                    reverse("logout"),
                ]
                if request.path not in allowed_urls:
                    return redirect("complete_profile")

        return self.get_response(request)
