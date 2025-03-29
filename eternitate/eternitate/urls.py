"""
URL configuration for eternitate project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView, RedirectView
from django.http import HttpResponse
from django.views.defaults import page_not_found

# Simple function to serve an empty response for favicon
def favicon_view(request):
    return HttpResponse(status=204)  # No content response

# Custom 404 handler
def handler404(request, exception):
    return page_not_found(request, exception, template_name="404.html")

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

# For testing the 404 template in development
if settings.DEBUG and getattr(settings, 'DEBUG_SHOW_CUSTOM_ERROR_PAGES', False):
    urlpatterns.append(path('test-404/', lambda request: handler404(request, Exception("Test 404 page"))))

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
