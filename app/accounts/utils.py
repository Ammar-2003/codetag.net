from django.core.mail import EmailMessage
import random
from django.conf import settings
from .models import User, OneTimePassword
from django.contrib.sites.shortcuts import get_current_site

def send_generated_otp_to_email(email, request): 
    subject = "One Time Passcode for Email Verification"
    otp = random.randint(1000, 9999)
    current_site = get_current_site(request).domain
    user = User.objects.get(email=email)
    
    # Save OTP to DB
    OneTimePassword.objects.update_or_create(user=user, defaults={'otp': otp})

    # Store email in session
    request.session['otp_email'] = email

    email_body = (
        f"Hi {user.first_name},\n\n"
        f"Thanks for signing up on {current_site}.\n"
        f"Please verify your email with this OTP: {otp}\n\n"
        "If you did not request this, please ignore this email."
    )
    
    email_msg = EmailMessage(
        subject=subject,
        body=email_body,
        from_email=settings.EMAIL_HOST_USER,
        to=[user.email]
    )
    email_msg.send()



def send_normal_email(data):
    email=EmailMessage(
        subject=data['email_subject'],
        body=data['email_body'],
        from_email=settings.EMAIL_HOST_USER,
        to=[data['to_email']]
    )
    email.send()
