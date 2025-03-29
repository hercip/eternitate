from django.contrib import admin
from .models import ProfileCode, Memorial, Photo, Video, TimelineEvent, Tribute


@admin.register(ProfileCode)
class ProfileCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'is_claimed', 'created_at')
    list_filter = ('is_claimed', 'created_at')
    search_fields = ('code',)
    date_hierarchy = 'created_at'


class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 1


class VideoInline(admin.TabularInline):
    model = Video
    extra = 1


class TimelineEventInline(admin.TabularInline):
    model = TimelineEvent
    extra = 1


@admin.register(Memorial)
class MemorialAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'owner', 'profile_code', 'birth_date', 'death_date', 'created_at')
    list_filter = ('allow_tributes', 'created_at')
    search_fields = ('full_name', 'owner__email', 'profile_code__code')
    date_hierarchy = 'created_at'
    inlines = [PhotoInline, VideoInline, TimelineEventInline]


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('memorial', 'caption', 'date_taken', 'order')
    list_filter = ('date_taken',)
    search_fields = ('memorial__full_name', 'caption')


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('memorial', 'caption', 'date_recorded', 'order')
    list_filter = ('date_recorded',)
    search_fields = ('memorial__full_name', 'caption')


@admin.register(TimelineEvent)
class TimelineEventAdmin(admin.ModelAdmin):
    list_display = ('memorial', 'title', 'date')
    list_filter = ('date',)
    search_fields = ('memorial__full_name', 'title', 'description')
    date_hierarchy = 'date'


@admin.register(Tribute)
class TributeAdmin(admin.ModelAdmin):
    list_display = ('memorial', 'name', 'email', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('memorial__full_name', 'name', 'email', 'message')
    date_hierarchy = 'created_at'
    actions = ['approve_tributes', 'unapprove_tributes']
    
    def approve_tributes(self, request, queryset):
        queryset.update(is_approved=True)
    approve_tributes.short_description = "Approve selected tributes"
    
    def unapprove_tributes(self, request, queryset):
        queryset.update(is_approved=False)
    unapprove_tributes.short_description = "Unapprove selected tributes"
