from django.urls import path
from . import views

app_name = 'memorials'

urlpatterns = [
    path('enter-code/', views.enter_code, name='enter_code'),
    path('generate-code/', views.generate_new_code, name='generate_new_code'),
    path('<str:code>/', views.memorial_detail, name='memorial_detail'),
    path('<str:code>/register/', views.register_memorial, name='register_memorial'),
    path('<str:code>/edit/', views.edit_memorial, name='edit_memorial'),
    path('<str:code>/photos/', views.upload_photo, name='upload_photo'),
    path('<str:code>/videos/', views.upload_video, name='upload_video'),
    path('<str:code>/timeline/', views.add_timeline_event, name='add_timeline_event'),
    path('<str:code>/tributes/', views.manage_tributes, name='manage_tributes'),
    path('<str:code>/toggle-tributes/', views.toggle_tributes, name='toggle_tributes'),
    path('photos/delete/<int:photo_id>/', views.delete_photo, name='delete_photo'),
    path('videos/delete/<int:video_id>/', views.delete_video, name='delete_video'),
    path('timeline/delete/<int:event_id>/', views.delete_event, name='delete_event'),
]
