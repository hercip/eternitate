from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from memorials.models import ProfileCode
import re
import uuid


class MemorialCodeAccountAdapter(DefaultAccountAdapter):
    """
    Custom adapter for django-allauth that extracts the memorial code from the URL
    and adds it to the redirect URL after signup.
    """
    
    def get_memorial_code_from_request(self, request):
        """Extract memorial code from the 'next' parameter in the request"""
        next_url = request.GET.get('next', '')
        if next_url:
            # Try to extract memorial code from URLs like 
            # /vHWgbuok8SCyGdCH7cF8TtlGN2RSsRmR/register/
            match = re.search(r'/([a-zA-Z0-9]{32})/register/', next_url)
            if match:
                return match.group(1)
        return None
    
    def is_open_for_signup(self, request):
        """
        Controls whether the site is open for signups.
        
        We'll always return True here, since we're handling the logic in the 
        signup_closed view. This prevents django-allauth from redirecting users
        away from the signup page when they have a valid memorial code.
        """
        return True
    
    def populate_username(self, request, user):
        """
        Fills in a valid username for our user, since allauth with email
        authentication still requires unique usernames.
        """
        # Use the first part of the email address as base for username
        email_base = user.email.split('@')[0]
        
        # Make username safe by removing special characters and limiting length
        safe_base = ''.join(c for c in email_base if c.isalnum())[:25]
        
        # Add a unique suffix to avoid collisions
        unique_id = str(uuid.uuid4())[:8]
        username = f"{safe_base}_{unique_id}"
        
        return username
    
    def save_user(self, request, user, form, commit=True):
        """
        This is called when saving user via allauth registration.
        We're saving user model fields that allauth doesn't save.
        """
        user = super().save_user(request, user, form, commit=False)
        
        # Generate unique username
        user.username = self.populate_username(request, user)
        
        # Get first and last name from form if present
        if hasattr(form, 'cleaned_data'):
            user.first_name = form.cleaned_data.get('first_name', '')
            user.last_name = form.cleaned_data.get('last_name', '')
        
        if commit:
            user.save()
        
        return user
        
    def get_signup_redirect_url(self, request):
        """
        Returns the URL to redirect to after successful signup.
        If there's a memorial code in the URL, redirect to register_memorial.
        """
        memorial_code = self.get_memorial_code_from_request(request)
        if memorial_code:
            return reverse('memorials:register_memorial', kwargs={'code': memorial_code})
        return super().get_signup_redirect_url(request)
        
    def pre_social_login(self, request, sociallogin):
        """Invoked just after a user successfully logs in using a social account."""
        # Check if we have a next URL with a memorial code
        memorial_code = self.get_memorial_code_from_request(request)
        if memorial_code:
            # Store the memorial code in the session for later use
            request.session['memorial_code'] = memorial_code