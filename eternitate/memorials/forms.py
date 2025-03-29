from django import forms
from .models import Memorial, Photo, Video, TimelineEvent, Tribute, ProfileCode


class MemorialCodeForm(forms.Form):
    """Form for entering a memorial code"""
    code = forms.CharField(
        max_length=32, 
        min_length=32, 
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Enter 32-character memorial code'
        }),
        error_messages={
            'required': 'Please enter a memorial code.',
            'min_length': 'The memorial code should be 32 characters long.',
            'max_length': 'The memorial code should be 32 characters long.',
        }
    )
    
    def clean_code(self):
        code = self.cleaned_data.get('code')
        if code:
            # Check if the code exists
            try:
                profile_code = ProfileCode.objects.get(code=code)
            except ProfileCode.DoesNotExist:
                raise forms.ValidationError("Invalid memorial code. Please check and try again.")
        return code


class MemorialRegistrationForm(forms.ModelForm):
    """Form for registering a new memorial using a profile code"""
    class Meta:
        model = Memorial
        fields = ['full_name', 'birth_date', 'death_date']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Enter full name'
            }),
            'birth_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500'
            }),
            'death_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500'
            }),
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
