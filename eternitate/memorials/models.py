from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify


class ProfileCode(models.Model):
    """Model to store the unique 32-character profile codes"""
    code = models.CharField(max_length=32, unique=True)
    is_claimed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        status = "Claimed" if self.is_claimed else "Unclaimed"
        return f"{self.code} ({status})"


class Memorial(models.Model):
    """Main model for digital memorials"""
    owner = models.ForeignKey(User, related_name='memorials', on_delete=models.CASCADE)
    profile_code = models.OneToOneField(ProfileCode, on_delete=models.CASCADE, related_name='memorial')
    
    # Basic information
    full_name = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    death_date = models.DateField(null=True, blank=True)
    
    # Profile and background images
    profile_image = models.ImageField(upload_to='memorials/profile_images/%Y/%m/', null=True, blank=True, 
                                      help_text="Profile photo of the person being commemorated")
    background_image = models.ImageField(upload_to='memorials/background_images/%Y/%m/', null=True, blank=True,
                                         help_text="Background image for the memorial page header")
    
    # Biography
    biography = models.TextField(blank=True)
    
    # Settings
    allow_tributes = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Memorial for {self.full_name}"
    
    def get_absolute_url(self):
        return reverse('memorials:memorial_detail', args=[str(self.profile_code.code)])


class Photo(models.Model):
    """Model for memorial photos"""
    memorial = models.ForeignKey(Memorial, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='memorials/photos/%Y/%m/')
    caption = models.CharField(max_length=255, blank=True)
    date_taken = models.DateField(null=True, blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', '-date_taken']
    
    def __str__(self):
        return f"Photo for {self.memorial.full_name}"


class Video(models.Model):
    """Model for memorial videos"""
    memorial = models.ForeignKey(Memorial, related_name='videos', on_delete=models.CASCADE)
    video = models.FileField(upload_to='memorials/videos/%Y/%m/')
    caption = models.CharField(max_length=255, blank=True)
    date_recorded = models.DateField(null=True, blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', '-date_recorded']
    
    def __str__(self):
        return f"Video for {self.memorial.full_name}"


class TimelineEvent(models.Model):
    """Model for timeline events"""
    memorial = models.ForeignKey(Memorial, related_name='timeline_events', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date = models.DateField()
    image = models.ImageField(upload_to='memorials/timeline/%Y/%m/', null=True, blank=True)
    
    class Meta:
        ordering = ['date']
    
    def __str__(self):
        return f"{self.title} - {self.date}"


class Tribute(models.Model):
    """Model for tributes/comments left by visitors"""
    memorial = models.ForeignKey(Memorial, related_name='tributes', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    message = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Tribute from {self.name} for {self.memorial.full_name}"
