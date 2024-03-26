# forms.py
from django import forms

class ContactForm(forms.Form):
    email = forms.EmailField(label='Your Email Address')
    title = forms.CharField(label='Message Title')
    message = forms.CharField(widget=forms.Textarea, label='Message')