from django.contrib import admin
from django.utils.html import format_html

from .models import Video


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    """Административная панель для модели Video"""
    list_display = [
        'preview_thumbnail',
        'title',
        'display_topics',
        'is_hidden',
        'likes_count_display',
        'dislikes_count_display',
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
        'likes_count_display',
        'dislikes_count_display',
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

    def likes_count_display(
        self,
        obj: Video,
    ) -> int:
        """Отображает количество лайков"""
        return obj.likes_count

    likes_count_display.short_description = 'Лайки'

    def dislikes_count_display(
        self,
        obj: Video,
    ) -> int:
        """Отображает количество дизлайков"""
        return obj.dislikes_count

    dislikes_count_display.short_description = 'Дизлайки'
