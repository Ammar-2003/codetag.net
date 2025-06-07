# accounts/middleware.py
from django.utils import timezone
from datetime import timedelta

class RegistrationSessionCleanupMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'user_registered' in request.session:
            # Clear if older than 7 days
            if timezone.now() - request.session.get('reg_time', timezone.now()) > timedelta(days=7):
                del request.session['user_registered']
                if 'registering_email' in request.session:
                    del request.session['registering_email']
        return self.get_response(request)