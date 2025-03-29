#!/usr/bin/env python
"""
Run script for the Eternitate application.
This script sets up the development server on port 8000 and 
configures the application to be externally accessible.
"""

import os
import sys
import random
import string
from django.core.management import execute_from_command_line
from django.core.management.commands.runserver import Command as RunServerCommand

# Apply monkey patch to default port
RunServerCommand.default_port = "8000"
RunServerCommand.default_addr = "0.0.0.0"

# Set up the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eternitate.settings')

# Generate a temporary secret key if not set
if os.environ.get('SECRET_KEY') is None:
    # Generate a random 50-character secret key
    secret_key = ''.join(random.choices(
        string.ascii_letters + string.digits + string.punctuation, 
        k=50
    ))
    os.environ['SECRET_KEY'] = secret_key

# Set DEBUG to True for development
os.environ.setdefault('DEBUG', 'True')

# Set environment variable to show custom error pages when accessing test-404
# This will be picked up by settings.py and temporarily disable DEBUG mode
os.environ.setdefault('SHOW_CUSTOM_ERROR_PAGES', 'True')

# Allow all hosts for development
os.environ.setdefault('ALLOWED_HOSTS', '*')

def main():
    """Run administrative tasks."""
    # Check if we need to generate sample profile codes
    if '--generate-codes' in sys.argv:
        sys.argv.remove('--generate-codes')
        from django.core.wsgi import get_wsgi_application
        application = get_wsgi_application()
        
        # Import needed models
        from memorials.models import ProfileCode
        
        # Generate 10 profile codes for testing
        for _ in range(10):
            code = ''.join(random.choices(
                string.ascii_uppercase + string.ascii_lowercase + string.digits,
                k=32
            ))
            if not ProfileCode.objects.filter(code=code).exists():
                ProfileCode.objects.create(code=code)
                print(f"Created profile code: {code}")
        
        print("Profile codes generated successfully!")
    
    # Start the development server with proper settings
    if len(sys.argv) <= 1:
        sys.argv.append('runserver')
        sys.argv.append('0.0.0.0:8000')
    
    # First initialize Django to prevent AppRegistryNotReady
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    
    # Apply migrations automatically if not explicitly running migrations
    if sys.argv[1] not in ['makemigrations', 'migrate', 'showmigrations']:
        from django.core.management import call_command
        call_command('makemigrations')
        call_command('migrate')
    
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
