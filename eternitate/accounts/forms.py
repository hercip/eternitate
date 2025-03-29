from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from allauth.account.forms import LoginForm, SignupForm
import requests


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add styling to the fields
        self.fields['login'].widget.attrs.update({
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Email address'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Password'
        })
        self.fields['remember'].widget.attrs.update({
            'class': 'h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded'
        })
    
    def clean(self):
        super().clean()
        # Add reCAPTCHA validation here if you want to validate reCAPTCHA on login form
        return self.cleaned_data
    

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(
        max_length=30, 
        label='First Name', 
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'First Name'
        })
    )
    last_name = forms.CharField(
        max_length=30, 
        label='Last Name', 
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Last Name'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add styling to the fields
        self.fields['email'].widget.attrs.update({
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Email address'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Confirm Password'
        })
    
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
