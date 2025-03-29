from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.contrib import messages
from django.urls import reverse
from .models import ProfileCode, Memorial, Photo, Video, TimelineEvent, Tribute
from .forms import (
    MemorialRegistrationForm, MemorialEditForm, PhotoForm,
    VideoForm, TimelineEventForm, TributeForm, MemorialCodeForm
)
from .utils import generate_profile_code


def memorial_detail(request, code):
    """View for displaying a memorial profile"""
    try:
        profile_code = ProfileCode.objects.get(code=code)
        
        # If the code exists but is not claimed yet, redirect to registration
        if not profile_code.is_claimed:
            return redirect('memorials:register_memorial', code=code)
        
        # Get the memorial associated with the profile code
        memorial = profile_code.memorial
        
        # Get photos, videos, timeline events, and approved tributes
        photos = memorial.photos.all()
        videos = memorial.videos.all()
        timeline_events = memorial.timeline_events.all().order_by('date')
        tributes = memorial.tributes.filter(is_approved=True)
        
        # Handle new tribute submission
        if request.method == 'POST' and memorial.allow_tributes:
            tribute_form = TributeForm(request.POST)
            if tribute_form.is_valid():
                tribute = tribute_form.save(commit=False)
                tribute.memorial = memorial
                tribute.save()
                messages.success(request, "Your tribute has been submitted and is pending approval.")
                return redirect('memorials:memorial_detail', code=code)
        else:
            tribute_form = TributeForm()
        
        context = {
            'memorial': memorial,
            'photos': photos,
            'videos': videos,
            'timeline_events': timeline_events,
            'tributes': tributes,
            'tribute_form': tribute_form,
            'is_owner': request.user.is_authenticated and request.user == memorial.owner,
        }
        
        return render(request, 'memorials/memorial_detail.html', context)
        
    except ProfileCode.DoesNotExist:
        # If the code doesn't exist, return 404 page not found
        raise Http404("Memorial page not found. The memorial code you entered does not exist.")


@login_required
def register_memorial(request, code):
    """View for registering a new memorial with a profile code"""
    # We use get_object_or_404 to return a 404 if the code doesn't exist
    profile_code = get_object_or_404(ProfileCode, code=code)
    
    # If the code is already claimed, redirect to the memorial
    if profile_code.is_claimed:
        return redirect('memorials:memorial_detail', code=code)
    
    if request.method == 'POST':
        form = MemorialRegistrationForm(request.POST)
        if form.is_valid():
            memorial = form.save(commit=False)
            memorial.owner = request.user
            memorial.profile_code = profile_code
            memorial.save()
            
            # Mark the profile code as claimed
            profile_code.is_claimed = True
            profile_code.save()
            
            messages.success(request, f"Memorial for {memorial.full_name} has been created.")
            return redirect('memorials:memorial_detail', code=code)
    else:
        form = MemorialRegistrationForm()
    
    return render(request, 'memorials/register_memorial.html', {'form': form, 'code': code})


@login_required
def edit_memorial(request, code):
    """View for editing a memorial"""
    profile_code = get_object_or_404(ProfileCode, code=code, is_claimed=True)
    memorial = get_object_or_404(Memorial, profile_code=profile_code)
    
    # Check if the user is the owner of this memorial
    if request.user != memorial.owner:
        messages.error(request, "You don't have permission to edit this memorial.")
        return redirect('memorials:memorial_detail', code=code)
    
    if request.method == 'POST':
        form = MemorialEditForm(request.POST, instance=memorial)
        if form.is_valid():
            form.save()
            messages.success(request, "Memorial updated successfully.")
            return redirect('memorials:memorial_detail', code=code)
    else:
        form = MemorialEditForm(instance=memorial)
    
    return render(request, 'memorials/edit_memorial.html', {'form': form, 'memorial': memorial})


@login_required
def upload_photo(request, code):
    """View for uploading photos to a memorial"""
    profile_code = get_object_or_404(ProfileCode, code=code, is_claimed=True)
    memorial = get_object_or_404(Memorial, profile_code=profile_code)
    
    # Check if the user is the owner of this memorial
    if request.user != memorial.owner:
        messages.error(request, "You don't have permission to add photos to this memorial.")
        return redirect('memorials:memorial_detail', code=code)
    
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.memorial = memorial
            photo.save()
            messages.success(request, "Photo uploaded successfully.")
            return redirect('memorials:upload_photo', code=code)
    else:
        form = PhotoForm()
    
    return render(request, 'memorials/photo_gallery.html', {
        'form': form, 
        'memorial': memorial,
        'photos': memorial.photos.all(),
    })


@login_required
def delete_photo(request, photo_id):
    """View for deleting a photo"""
    photo = get_object_or_404(Photo, id=photo_id)
    memorial = photo.memorial
    
    # Check if the user is the owner of this memorial
    if request.user != memorial.owner:
        messages.error(request, "You don't have permission to delete photos from this memorial.")
        return redirect('memorials:memorial_detail', code=memorial.profile_code.code)
    
    if request.method == 'POST':
        photo.delete()
        messages.success(request, "Photo deleted successfully.")
    
    return redirect('memorials:upload_photo', code=memorial.profile_code.code)


@login_required
def upload_video(request, code):
    """View for uploading videos to a memorial"""
    profile_code = get_object_or_404(ProfileCode, code=code, is_claimed=True)
    memorial = get_object_or_404(Memorial, profile_code=profile_code)
    
    # Check if the user is the owner of this memorial
    if request.user != memorial.owner:
        messages.error(request, "You don't have permission to add videos to this memorial.")
        return redirect('memorials:memorial_detail', code=code)
    
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.memorial = memorial
            video.save()
            messages.success(request, "Video uploaded successfully.")
            return redirect('memorials:upload_video', code=code)
    else:
        form = VideoForm()
    
    return render(request, 'memorials/video_gallery.html', {
        'form': form, 
        'memorial': memorial,
        'videos': memorial.videos.all(),
    })


@login_required
def delete_video(request, video_id):
    """View for deleting a video"""
    video = get_object_or_404(Video, id=video_id)
    memorial = video.memorial
    
    # Check if the user is the owner of this memorial
    if request.user != memorial.owner:
        messages.error(request, "You don't have permission to delete videos from this memorial.")
        return redirect('memorials:memorial_detail', code=memorial.profile_code.code)
    
    if request.method == 'POST':
        video.delete()
        messages.success(request, "Video deleted successfully.")
    
    return redirect('memorials:upload_video', code=memorial.profile_code.code)


@login_required
def add_timeline_event(request, code):
    """View for adding timeline events to a memorial"""
    profile_code = get_object_or_404(ProfileCode, code=code, is_claimed=True)
    memorial = get_object_or_404(Memorial, profile_code=profile_code)
    
    # Check if the user is the owner of this memorial
    if request.user != memorial.owner:
        messages.error(request, "You don't have permission to add timeline events to this memorial.")
        return redirect('memorials:memorial_detail', code=code)
    
    if request.method == 'POST':
        form = TimelineEventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.memorial = memorial
            event.save()
            messages.success(request, "Timeline event added successfully.")
            return redirect('memorials:add_timeline_event', code=code)
    else:
        form = TimelineEventForm()
    
    return render(request, 'memorials/timeline.html', {
        'form': form, 
        'memorial': memorial,
        'events': memorial.timeline_events.all().order_by('date'),
    })


@login_required
def delete_event(request, event_id):
    """View for deleting a timeline event"""
    event = get_object_or_404(TimelineEvent, id=event_id)
    memorial = event.memorial
    
    # Check if the user is the owner of this memorial
    if request.user != memorial.owner:
        messages.error(request, "You don't have permission to delete timeline events from this memorial.")
        return redirect('memorials:memorial_detail', code=memorial.profile_code.code)
    
    if request.method == 'POST':
        event.delete()
        messages.success(request, "Timeline event deleted successfully.")
    
    return redirect('memorials:add_timeline_event', code=memorial.profile_code.code)


@login_required
def manage_tributes(request, code):
    """View for managing tributes on a memorial"""
    profile_code = get_object_or_404(ProfileCode, code=code, is_claimed=True)
    memorial = get_object_or_404(Memorial, profile_code=profile_code)
    
    # Check if the user is the owner of this memorial
    if request.user != memorial.owner:
        messages.error(request, "You don't have permission to manage tributes for this memorial.")
        return redirect('memorials:memorial_detail', code=code)
    
    tributes = memorial.tributes.all().order_by('-created_at')
    
    # Handle approval/rejection actions
    if request.method == 'POST':
        tribute_id = request.POST.get('tribute_id')
        action = request.POST.get('action')
        
        if tribute_id and action:
            tribute = get_object_or_404(Tribute, id=tribute_id, memorial=memorial)
            
            if action == 'approve':
                tribute.is_approved = True
                tribute.save()
                messages.success(request, "Tribute approved.")
            elif action == 'reject':
                tribute.delete()
                messages.success(request, "Tribute deleted.")
            
            return redirect('memorials:manage_tributes', code=code)
    
    return render(request, 'memorials/tributes.html', {
        'memorial': memorial,
        'tributes': tributes,
    })


@login_required
def toggle_tributes(request, code):
    """View for toggling the allow_tributes setting"""
    profile_code = get_object_or_404(ProfileCode, code=code, is_claimed=True)
    memorial = get_object_or_404(Memorial, profile_code=profile_code)
    
    # Check if the user is the owner of this memorial
    if request.user != memorial.owner:
        messages.error(request, "You don't have permission to change settings for this memorial.")
        return redirect('memorials:memorial_detail', code=code)
    
    if request.method == 'POST':
        memorial.allow_tributes = not memorial.allow_tributes
        memorial.save()
        
        if memorial.allow_tributes:
            messages.success(request, "Tributes have been enabled.")
        else:
            messages.success(request, "Tributes have been disabled.")
    
    return redirect('memorials:manage_tributes', code=code)


def enter_code(request):
    """View for entering a memorial code"""
    # Check if code is provided in the URL query parameters
    code = request.GET.get('code')
    if code:
        # Validate the code format
        if len(code) == 32:
            # Check if the code exists
            try:
                profile_code = ProfileCode.objects.get(code=code)
                
                # If the code is claimed, go directly to the memorial
                if profile_code.is_claimed:
                    return redirect('memorials:memorial_detail', code=code)
                
                # If the code is not claimed and user is not logged in, redirect to login
                if not request.user.is_authenticated:
                    messages.info(request, "Please log in to register this memorial.")
                    return redirect(f"{reverse('account_login')}?next={reverse('memorials:register_memorial', kwargs={'code': code})}")
                
                # If user is logged in, go to registration
                return redirect('memorials:register_memorial', code=code)
                
            except ProfileCode.DoesNotExist:
                # Code doesn't exist, show error
                messages.error(request, "Invalid memorial code. Please check and try again or contact support.")
        else:
            messages.error(request, "Invalid memorial code format. The code should be 32 characters long.")
    
    if request.method == 'POST':
        form = MemorialCodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            return redirect(f"{reverse('memorials:enter_code')}?code={code}")
    else:
        form = MemorialCodeForm()
    
    return render(request, 'memorials/enter_code.html', {'form': form})


@login_required
def generate_new_code(request):
    """View for generating a new profile code"""
    # Generate a new profile code
    code = generate_profile_code()
    profile_code = ProfileCode.objects.create(code=code)
    
    messages.success(request, f"New profile code generated: {code}")
    return redirect('memorials:register_memorial', code=code)
