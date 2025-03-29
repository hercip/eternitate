from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import FormView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from .forms import CustomSignupForm, CustomLoginForm
from memorials.models import Memorial


@login_required
def profile_view(request):
    """View for user profile page"""
    # Get all memorials owned by the user
    user_memorials = Memorial.objects.filter(owner=request.user)
    
    context = {
        'user': request.user,
        'memorials': user_memorials,
    }
    return render(request, 'accounts/profile.html', context)


def signup_closed(request):
    """View that redirects users from direct signup to the code entry page"""
    # Check if we have a 'next' parameter with a memorial code
    next_url = request.GET.get('next', '')
    if next_url and '/register/' in next_url:
        import re
        match = re.search(r'/([a-zA-Z0-9]{32})/register/', next_url)
        if match:
            # We have a memorial code in the URL, we can use it
            code = match.group(1)
            # Verify the code is valid
            try:
                from memorials.models import ProfileCode
                profile_code = ProfileCode.objects.get(code=code)
                if not profile_code.is_claimed:
                    # Code is valid and not claimed, allow signup
                    from django.shortcuts import redirect
                    return redirect(f"/accounts/signup/?next={next_url}")
            except ProfileCode.DoesNotExist:
                # Code doesn't exist, we'll create it during signup
                from django.shortcuts import redirect
                return redirect(f"/accounts/signup/?next={next_url}")
    
    messages.info(request, "To create an account, you need a valid memorial code.")
    return render(request, 'account/signup_closed.html')
