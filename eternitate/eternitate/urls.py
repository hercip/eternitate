"""
URL configuration for eternitate project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView, RedirectView
from django.http import HttpResponse

# Simple function to serve an empty response for favicon
def favicon_view(request):
    return HttpResponse(status=204)  # No content response

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('favicon.ico', favicon_view),  # Handle favicon.ico requests without trailing slash
    path('favicon.ico/', favicon_view),  # Handle favicon.ico requests with trailing slash
    path('favicon.ico/register/', favicon_view),  # Handle favicon.ico/register/ requests
    path('', include('memorials.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
