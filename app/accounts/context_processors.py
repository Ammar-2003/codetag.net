# accounts/context_processors.py
def auth_status(request):
    return {
        'user_registered': request.session.get('user_registered', False)
    }