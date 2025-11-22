from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
)
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.conf import settings
from conf.logger import log_user_action
from videos.models import Video, VideoRating, Topic


def video_list(request: HttpRequest) -> HttpResponse:
    """
    Отображает список видео с постраничным просмотром
    и фильтрацией по темам
    """
    # Получаем параметры фильтрации по темам (может быть несколько)
    topic_slugs = request.GET.getlist('topic')
    active_topics = []

    # Базовый queryset - только не скрытые видео
    videos = Video.objects.filter(is_hidden=False).order_by('-created_at')

    # Если выбраны темы - фильтруем по ним
    if topic_slugs:
        # Получаем объекты тем по slug
        topics_queryset = Topic.objects.filter(slug__in=topic_slugs)
        active_topics = list(topics_queryset)

        # Фильтруем видео: показываем те, у которых есть хотя бы одна
        # из выбранных тем
        if active_topics:
            videos = videos.filter(topics__in=active_topics).distinct()

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

    # Получаем все темы для отображения фильтров
    all_topics = Topic.objects.all().order_by('name')

    context = {
        'page_obj': page_obj,
        'videos': page_obj,
        'user_ratings': user_ratings,
        'topics': all_topics,
        'active_topics': active_topics,
        'active_topic_slugs': topic_slugs,
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
            log_user_action(
                request.user,
                f'Снял лайк с видео "{video.title}"',
            )
        # Если есть дизлайк - меняем на лайк
        else:
            rating.rating_type = 'like'
            rating.save()
            log_user_action(
                request.user,
                f'Изменил дизлайк на лайк для видео "{video.title}"',
            )
    except VideoRating.DoesNotExist:
        # Создаем новый лайк
        VideoRating.objects.create(
            video=video,
            user=request.user,
            rating_type='like',
        )
        log_user_action(
            request.user,
            f'Поставил лайк видео "{video.title}"',
        )

    # Сохраняем параметры фильтрации по темам при редиректе
    topic_slugs = request.GET.getlist('topic')
    if topic_slugs:
        topic_params = '&'.join([f'topic={slug}' for slug in topic_slugs])
        return redirect(f'{reverse("videos:video_list")}?{topic_params}')
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
            log_user_action(
                request.user,
                f'Снял дизлайк с видео "{video.title}"',
            )
        # Если есть лайк - меняем на дизлайк
        else:
            rating.rating_type = 'dislike'
            rating.save()
            log_user_action(
                request.user,
                f'Изменил лайк на дизлайк для видео "{video.title}"',
            )
    except VideoRating.DoesNotExist:
        # Создаем новый дизлайк
        VideoRating.objects.create(
            video=video,
            user=request.user,
            rating_type='dislike',
        )
        log_user_action(
            request.user,
            f'Поставил дизлайк видео "{video.title}"',
        )

    # Сохраняем параметры фильтрации по темам при редиректе
    topic_slugs = request.GET.getlist('topic')
    if topic_slugs:
        topic_params = '&'.join([f'topic={slug}' for slug in topic_slugs])
        return redirect(f'{reverse("videos:video_list")}?{topic_params}')
    return redirect('videos:video_list')
