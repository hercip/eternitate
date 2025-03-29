import random
import string
from .models import ProfileCode


def generate_profile_code():
    """Generate a unique 32-character profile code"""
    while True:
        # Generate a random 32-character string
        code = ''.join(random.choices(
            string.ascii_uppercase + string.ascii_lowercase + string.digits, 
            k=32
        ))
        
        # Check if the code already exists
        if not ProfileCode.objects.filter(code=code).exists():
            return code
