from django.contrib.auth import logout
from django.shortcuts import redirect
from django.utils import timezone

EXEMPT_PATHS = ("/expired/", "/login/", "/logout/")


class SubscriptionCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Agar foydalanuvchi login bo'lsa tekshir
        if request.user.is_authenticated:
            subscription_end = getattr(request.user, "subscription_end", None)
            is_active = getattr(request.user, "is_active", True)

            expired = (not is_active) or (subscription_end and subscription_end < timezone.now())
            if expired:
                # sessionni tozalaymiz — shunda login sahifasi ishlaydi
                logout(request)

                # Agar allaqachon expired/login/logout sahifasida bo'lmasa, yo'naltiramiz
                path = request.path
                if not any(path.startswith(p) for p in EXEMPT_PATHS):
                    return redirect("subscription_expired")
        return self.get_response(request)
