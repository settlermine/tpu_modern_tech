from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from urllib.parse import urlencode

from .models import (
    Video,
    VideoRating,
)


@admin.register(VideoRating)
class VideoRatingAdmin(admin.ModelAdmin):
    """Административная панель для модели VideoRating"""
    list_display = [
        'video',
        'user',
        'rating_type',
        'created_at',
    ]
    list_filter = [
        'rating_type',
        'video',
        'created_at',
    ]
    search_fields = [
        'video__title',
        'user__username',
    ]
    readonly_fields = [
        'video',
        'user',
        'rating_type',
        'created_at',
    ]
    list_per_page = 25

    def has_add_permission(
        self,
        request,
    ) -> bool:
        return False

    def has_delete_permission(
        self,
        request,
        obj=None,
    ) -> bool:
        return False

    def has_change_permission(
        self,
        request,
        obj=None,
    ) -> bool:
        return False


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    """Административная панель для модели Video"""
    list_display = [
        'preview_thumbnail',
        'title',
        'display_topics',
        'is_hidden',
        'ratings_link',
        'created_at',
    ]
    list_filter = [
        'is_hidden',
        'topics',
        'created_at',
    ]
    search_fields = ['title', 'source_url']
    readonly_fields = [
        'created_at',
        'updated_at',
        'ratings_link',
    ]
    list_per_page = 10
    filter_horizontal = ['topics']

    def preview_thumbnail(
        self,
        obj: Video,
    ) -> str:
        """Отображает миниатюру превью видео"""
        if obj.preview_image_url:
            return format_html(
                '<img src="{}" style="max-width: 100px; max-height: 60px;" />',
                obj.preview_image_url,
            )
        return '-'

    preview_thumbnail.short_description = 'Превью'

    def display_topics(
        self,
        obj: Video,
    ) -> str:
        """Отображает список тем видео"""
        topics = obj.topics.all()
        if topics:
            return ', '.join([topic.name for topic in topics])
        return '-'

    display_topics.short_description = 'Темы'

    def ratings_link(
        self,
        obj: Video,
    ) -> str:
        """Создает ссылку на отфильтрованный список оценок"""
        if not obj.pk:
            return '-'

        url = (
            reverse('admin:videos_videorating_changelist') +
            '?' +
            urlencode({'video__id__exact': obj.pk})
        )
        likes_count = obj.likes_count
        dislikes_count = obj.dislikes_count

        if likes_count == 0 and dislikes_count == 0:
            return format_html(
                '<span style="color: #999;">Нет оценок</span>'
            )

        text_parts = []
        if likes_count > 0:
            text_parts.append(f'👍 ({likes_count})')
        if dislikes_count > 0:
            text_parts.append(f'👎 ({dislikes_count})')

        return format_html(
            '<a href="{}" style="text-decoration: underline;">{}</a>',
            url,
            ', '.join(text_parts),
        )

    ratings_link.short_description = 'Оценки'
