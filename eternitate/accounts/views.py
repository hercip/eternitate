from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import FormView
from django.urls import reverse_lazy
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
