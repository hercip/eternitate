from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse
from django.http import HttpResponseRedirect
import re


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
    
    def get_signup_redirect_url(self, request):
        """
        Returns the URL to redirect to after successful signup.
        If there's a memorial code in the URL, redirect to register_memorial.
        """
        memorial_code = self.get_memorial_code_from_request(request)
        if memorial_code:
            return reverse('memorials:register_memorial', kwargs={'code': memorial_code})
        return super().get_signup_redirect_url(request)