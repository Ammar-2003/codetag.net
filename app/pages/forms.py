from django import forms

class HireMeForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    company = forms.CharField(max_length=100, required=False)
    message = forms.CharField(widget=forms.Textarea)

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=150)
    message = forms.CharField(widget=forms.Textarea)