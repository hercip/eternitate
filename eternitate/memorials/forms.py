from django import forms
from .models import Memorial, Photo, Video, TimelineEvent, Tribute


class MemorialRegistrationForm(forms.ModelForm):
    """Form for registering a new memorial using a profile code"""
    class Meta:
        model = Memorial
        fields = ['full_name', 'birth_date', 'death_date']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'death_date': forms.DateInput(attrs={'type': 'date'}),
        }


class MemorialEditForm(forms.ModelForm):
    """Form for editing memorial information"""
    class Meta:
        model = Memorial
        fields = ['full_name', 'birth_date', 'death_date', 'biography', 'allow_tributes']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'death_date': forms.DateInput(attrs={'type': 'date'}),
            'biography': forms.Textarea(attrs={'rows': 10}),
        }


class PhotoForm(forms.ModelForm):
    """Form for uploading photos"""
    class Meta:
        model = Photo
        fields = ['image', 'caption', 'date_taken', 'order']
        widgets = {
            'date_taken': forms.DateInput(attrs={'type': 'date'}),
        }


class VideoForm(forms.ModelForm):
    """Form for uploading videos"""
    class Meta:
        model = Video
        fields = ['video', 'caption', 'date_recorded', 'order']
        widgets = {
            'date_recorded': forms.DateInput(attrs={'type': 'date'}),
        }


class TimelineEventForm(forms.ModelForm):
    """Form for creating timeline events"""
    class Meta:
        model = TimelineEvent
        fields = ['title', 'description', 'date', 'image']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 5}),
        }


class TributeForm(forms.ModelForm):
    """Form for posting tributes"""
    class Meta:
        model = Tribute
        fields = ['name', 'email', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5}),
        }
