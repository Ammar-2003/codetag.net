from django.urls import path
from .views import HireMeView , PrivacyPolicyView, TermsOfServiceView , ContactView


urlpatterns = [
    path('hire-me/', HireMeView.as_view(), name='hire_me'),
    path('privacy-policy/', PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('terms-of-service/', TermsOfServiceView.as_view(), name='terms_of_service'),
    path('contact/', ContactView.as_view(), name='contact'),
]