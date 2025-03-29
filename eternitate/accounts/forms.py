from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from allauth.account.forms import LoginForm, SignupForm
import requests


class CustomLoginForm(LoginForm):
    def clean(self):
        super().clean()
        # Add reCAPTCHA validation here if you want to validate reCAPTCHA on login form
        return self.cleaned_data
    

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name', required=True)
    last_name = forms.CharField(max_length=30, label='Last Name', required=True)
    
    def clean(self):
        super().clean()
        # Add reCAPTCHA validation here
        return self.cleaned_data

    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user
