#!/usr/bin/env python
"""
Asset management script for Eternitate project.

This script provides utilities for:
1. Generating profile codes
2. Managing media files
3. Data migration and backup
"""

import os
import uuid
import django
import random
import string
import argparse
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eternitate.settings')
django.setup()

from memorials.models import ProfileCode, Memorial


def generate_profile_codes(count=10):
    """Generate a specified number of profile codes"""
    codes_created = 0
    
    for _ in range(count):
        # Generate a random 32-character code
        code = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
        
        # Check if the code already exists
        if not ProfileCode.objects.filter(code=code).exists():
            ProfileCode.objects.create(code=code)
            codes_created += 1
            print(f"Created profile code: {code}")
    
    print(f"Successfully created {codes_created} profile codes.")


def list_memorials():
    """List all memorials in the system"""
    memorials = Memorial.objects.all().select_related('owner', 'profile_code')
    
    if not memorials:
        print("No memorials found in the system.")
        return
    
    print("\nList of all memorials:")
    print("-" * 80)
    print(f"{'Name':<30} {'Owner':<20} {'Profile Code':<35} {'Created'}")
    print("-" * 80)
    
    for memorial in memorials:
        print(f"{memorial.full_name:<30} {memorial.owner.email:<20} {memorial.profile_code.code:<35} {memorial.created_at.strftime('%Y-%m-%d')}")
    
    print("-" * 80)


def list_profile_codes():
    """List all profile codes in the system"""
    codes = ProfileCode.objects.all()
    
    if not codes:
        print("No profile codes found in the system.")
        return
    
    print("\nList of all profile codes:")
    print("-" * 80)
    print(f"{'Code':<35} {'Status':<15} {'Created'}")
    print("-" * 80)
    
    for code in codes:
        status = "Claimed" if code.is_claimed else "Unclaimed"
        print(f"{code.code:<35} {status:<15} {code.created_at.strftime('%Y-%m-%d')}")
    
    print("-" * 80)


def backup_database():
    """Create a database backup using Django's dumpdata command"""
    backup_dir = os.path.join('backups')
    os.makedirs(backup_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = os.path.join(backup_dir, f'eternitate_backup_{timestamp}.json')
    
    os.system(f'python manage.py dumpdata --exclude auth.permission --exclude contenttypes --indent 2 > {backup_file}')
    
    print(f"Database backup created at {backup_file}")


def clear_unused_profile_codes(days=30):
    """Remove unclaimed profile codes older than the specified number of days"""
    cutoff_date = datetime.now() - timedelta(days=days)
    
    # Get unclaimed profile codes older than the cutoff date
    old_codes = ProfileCode.objects.filter(is_claimed=False, created_at__lt=cutoff_date)
    
    count = old_codes.count()
    if count > 0:
        old_codes.delete()
        print(f"Removed {count} unclaimed profile codes older than {days} days.")
    else:
        print(f"No unclaimed profile codes older than {days} days found.")


def print_help():
    """Display help information"""
    print("\nEternitate Asset Management Tool")
    print("=" * 40)
    print("Available commands:")
    print("  generate <count>         - Generate <count> new profile codes")
    print("  list-memorials           - List all memorials in the system")
    print("  list-codes               - List all profile codes in the system")
    print("  backup                   - Create a database backup")
    print("  clear-codes <days>       - Remove unclaimed profile codes older than <days> days")
    print("  help                     - Display this help message")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Eternitate Asset Management Tool')
    parser.add_argument('command', nargs='?', default='help', help='Command to execute')
    parser.add_argument('param', nargs='?', help='Optional parameter for the command')
    
    args = parser.parse_args()
    
    if args.command == 'generate':
        count = int(args.param) if args.param and args.param.isdigit() else 10
        generate_profile_codes(count)
    elif args.command == 'list-memorials':
        list_memorials()
    elif args.command == 'list-codes':
        list_profile_codes()
    elif args.command == 'backup':
        backup_database()
    elif args.command == 'clear-codes':
        days = int(args.param) if args.param and args.param.isdigit() else 30
        clear_unused_profile_codes(days)
    else:
        print_help()