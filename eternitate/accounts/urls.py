from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    # Custom signup closed view to handle memorial code redirects
    path('signup-closed/', views.signup_closed, name='signup_closed'),
]