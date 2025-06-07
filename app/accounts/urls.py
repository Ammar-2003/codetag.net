from django.urls import path, include
from .views import UserRegisterView , VerifyOTPView , UserLoginView, logout_view
from django.contrib.auth import views as auth_views
from .forms import CustomPasswordResetForm


urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('otp-verify/', VerifyOTPView.as_view(), name='otp-verify'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('', include('allauth.urls')), 
    # Password reset URLs
    path('password-reset/', 
     auth_views.PasswordResetView.as_view(
         template_name='accounts/password_reset.html',
         email_template_name='accounts/password_reset_email.html',
         subject_template_name='accounts/password_reset_subject.txt',
         form_class=CustomPasswordResetForm
     ), 
     name='password_reset'),
    
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/password_reset_done.html'
         ), 
         name='password_reset_done'),
    
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset_confirm.html'
         ), 
         name='password_reset_confirm'),
    
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/password_reset_complete.html'
         ), 
         name='password_reset_complete'),
]