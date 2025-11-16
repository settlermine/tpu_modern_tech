from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
)
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpRequest, HttpResponse
from django.conf import settings
from videos.models import Video, VideoRating


def video_list(request: HttpRequest) -> HttpResponse:
    """Отображает список видео с постраничным просмотром"""
    videos = Video.objects.filter(is_hidden=False).order_by('-created_at')

    paginator = Paginator(
        videos,
        settings.VIDEO_PAGINATION_SIZE,
    )
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # Получаем оценки текущего пользователя для всех видео на странице
    user_ratings = {}
    if request.user.is_authenticated:
        video_ids = [video.id for video in page_obj]
        ratings = VideoRating.objects.filter(
            video_id__in=video_ids,
            user=request.user,
        ).select_related('video')
        user_ratings = {
            rating.video_id: rating.rating_type
            for rating in ratings
        }

    context = {
        'page_obj': page_obj,
        'videos': page_obj,
        'user_ratings': user_ratings,
    }

    return render(
        request,
        'videos/video_list.html',
        context,
    )


@login_required
def like_video(
    request: HttpRequest,
    video_id: int,
) -> HttpResponse:
    """Обработка лайка видео"""
    video = get_object_or_404(
        Video,
        id=video_id,
        is_hidden=False,
    )

    # Проверяем, есть ли уже оценка от этого пользователя
    try:
        rating = VideoRating.objects.get(
            video=video,
            user=request.user,
        )
        # Если уже есть лайк - удаляем (снимаем лайк)
        if rating.rating_type == 'like':
            rating.delete()
        # Если есть дизлайк - меняем на лайк
        else:
            rating.rating_type = 'like'
            rating.save()
    except VideoRating.DoesNotExist:
        # Создаем новый лайк
        VideoRating.objects.create(
            video=video,
            user=request.user,
            rating_type='like',
        )

    return redirect('videos:video_list')


@login_required
def dislike_video(
    request: HttpRequest,
    video_id: int,
) -> HttpResponse:
    """Обработка дизлайка видео"""
    video = get_object_or_404(
        Video,
        id=video_id,
        is_hidden=False,
    )

    # Проверяем, есть ли уже оценка от этого пользователя
    try:
        rating = VideoRating.objects.get(
            video=video,
            user=request.user,
        )
        # Если уже есть дизлайк - удаляем (снимаем дизлайк)
        if rating.rating_type == 'dislike':
            rating.delete()
        # Если есть лайк - меняем на дизлайк
        else:
            rating.rating_type = 'dislike'
            rating.save()
    except VideoRating.DoesNotExist:
        # Создаем новый дизлайк
        VideoRating.objects.create(
            video=video,
            user=request.user,
            rating_type='dislike',
        )

    return redirect('videos:video_list')


class CustomLoginView(LoginView):
    """Кастомная страница входа"""
    template_name = 'videos/login.html'
    redirect_authenticated_user = True

    def get_success_url(self) -> str:
        return '/'
