#!/usr/bin/env python
"""
Asset management script for Eternitate project.

This script provides utilities for:
1. Generating profile codes
2. Managing media files
3. Data migration and backup
"""

import os
import sys
import random
import string
import django
from django.core.management import call_command

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eternitate.settings')
django.setup()

from memorials.models import ProfileCode, Memorial


def generate_profile_codes(count=10):
    """Generate a specified number of profile codes"""
    codes_created = 0
    
    for _ in range(count):
        # Generate a random 32-character code
        code = ''.join(random.choices(
            string.ascii_uppercase + string.ascii_lowercase + string.digits, 
            k=32
        ))
        
        # Check if the code already exists
        if not ProfileCode.objects.filter(code=code).exists():
            ProfileCode.objects.create(code=code)
            codes_created += 1
            print(f"Created code: {code}")
    
    print(f"Successfully created {codes_created} new profile codes.")


def list_memorials():
    """List all memorials in the system"""
    memorials = Memorial.objects.all().order_by('-created_at')
    
    if not memorials:
        print("No memorials found in the system.")
        return
    
    print(f"Found {memorials.count()} memorials:")
    print("-" * 80)
    
    for memorial in memorials:
        print(f"ID: {memorial.id}")
        print(f"Name: {memorial.full_name}")
        print(f"Owner: {memorial.owner.email}")
        print(f"Code: {memorial.profile_code.code}")
        print(f"Created: {memorial.created_at}")
        print("-" * 80)


def backup_database():
    """Create a database backup using Django's dumpdata command"""
    try:
        filename = f"eternitate_backup_{django.utils.timezone.now().strftime('%Y%m%d_%H%M%S')}.json"
        call_command('dumpdata', output=filename)
        print(f"Database backup created: {filename}")
    except Exception as e:
        print(f"Error creating database backup: {e}")


def clear_unused_profile_codes(days=30):
    """Remove unclaimed profile codes older than the specified number of days"""
    from django.utils import timezone
    import datetime
    
    cutoff_date = timezone.now() - datetime.timedelta(days=days)
    codes = ProfileCode.objects.filter(is_claimed=False, created_at__lt=cutoff_date)
    
    if not codes:
        print(f"No unclaimed profile codes older than {days} days found.")
        return
    
    count = codes.count()
    codes.delete()
    print(f"Deleted {count} unclaimed profile codes older than {days} days.")


def print_help():
    """Display help information"""
    print("Eternitate Asset Management Utility")
    print("=" * 40)
    print("Available commands:")
    print("  generate-codes [count]   - Generate new profile codes (default: 10)")
    print("  list-memorials           - List all memorials in the system")
    print("  backup                   - Create a database backup")
    print("  clear-unused [days]      - Clear unused profile codes (default: 30 days)")
    print("  help                     - Show this help message")


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] == "help":
        print_help()
    elif sys.argv[1] == "generate-codes":
        count = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        generate_profile_codes(count)
    elif sys.argv[1] == "list-memorials":
        list_memorials()
    elif sys.argv[1] == "backup":
        backup_database()
    elif sys.argv[1] == "clear-unused":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        clear_unused_profile_codes(days)
    else:
        print(f"Unknown command: {sys.argv[1]}")
        print_help()
