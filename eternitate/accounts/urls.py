from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    # Custom signup view to override allauth's
    path('signup/', views.signup_closed, name='signup_closed'),
]