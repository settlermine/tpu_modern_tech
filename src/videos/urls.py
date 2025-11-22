from django.urls import path
from videos import views

app_name = 'videos'

urlpatterns = [
    path('', views.video_list, name='video_list'),
    path(
        'video/<int:video_id>/like/',
        views.like_video,
        name='like_video',
    ),
    path(
        'video/<int:video_id>/dislike/',
        views.dislike_video,
        name='dislike_video',
    ),
]
