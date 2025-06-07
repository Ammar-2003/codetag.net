from django.views.generic.edit import FormView
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import HireMeForm
from django.views.generic import TemplateView
from .forms import ContactForm
from django.template.loader import render_to_string


# Create your views here.
class HireMeView(FormView):
    template_name = 'pages/hire_me.html'
    form_class = HireMeForm
    success_url = reverse_lazy('hire_me')  # Make sure this URL name exists

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'your_target_role': 'Python Backend Developer',
            'your_short_bio': ' A Software Engineer expertise in Python Backend Development . Currently building scalable real world applications.',
            'key_skills': [
                'Python Backend Development',
                'Django',
                'Django Rest Framework',
                'FastAPI',
                'Cloud Deployment (AWS/GCP)'
            ],
            'your_availability_status': 'Available immediately',
            'your_location_preference': 'Onsite in UAE',
            'your_linkedin_url': 'https://www.linkedin.com/in/muhammad-ammar-335261321/'
        })
        return context

    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        company = form.cleaned_data.get('company', 'Not specified')
        message = form.cleaned_data['message']

        send_mail(
            f'Hire Me Inquiry from {name}',
            f"Name: {name}\nEmail: {email}\nCompany: {company}\n\nMessage:\n{message}",
            settings.DEFAULT_FROM_EMAIL,
            [settings.CONTACT_EMAIL],
            fail_silently=False,
        )

        messages.success(self.request, 'Thank you! Your message has been sent. I will respond soon.')
        return super().form_valid(form)
    
class ContactView(FormView):
    template_name = 'pages/contact_us.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact')

    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']

        # Admin email
        email_subject = f"New Contact Form Submission: {subject}"
        email_body = render_to_string('pages/contact_form.txt', {
            'name': name,
            'email': email,
            'subject': subject,
            'message': message,
        })
        send_mail(
            email_subject,
            email_body,
            settings.DEFAULT_FROM_EMAIL,
            [settings.CONTACT_EMAIL],
            fail_silently=False,
        )

        # Confirmation email to user
        user_subject = "Thank you for contacting codetag.net"
        user_body = render_to_string('pages/contact_confirmation.txt', {
            'name': name,
        })
        send_mail(
            user_subject,
            user_body,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        messages.success(self.request, 'Thank you for your message! We will get back to you soon.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please fill in all required fields.')
        return super().form_invalid(form)
    
class PrivacyPolicyView(TemplateView):
    template_name = 'pages/privacy_policy.html'

class TermsOfServiceView(TemplateView):
    template_name = 'pages/terms_of_service.html'