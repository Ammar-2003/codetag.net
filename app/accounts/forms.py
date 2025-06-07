from django import forms
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordResetForm

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email
    
class OTPVerificationForm(forms.Form):
    otp = forms.CharField(
        label="One-Time Passcode",
        max_length=6,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter OTP'
        })
    )

class LoginForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=155)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class CustomPasswordResetForm(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise ValidationError("There is no user registered with this email address.")
        return email