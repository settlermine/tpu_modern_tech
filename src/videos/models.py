from django.db import models
from django.contrib.auth.models import User


class Topic(models.Model):
    """Модель для хранения тем видео"""
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Название темы',
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name='URL-слаг',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class Video(models.Model):
    """Модель для хранения информации о видео"""
    title = models.CharField(
        max_length=200,
        verbose_name='Название видео'
    )
    preview_image_url = models.URLField(
        verbose_name='Превью-картинка (ссылка)'
    )
    source_url = models.URLField(
        verbose_name='Ссылка на источник'
    )
    is_hidden = models.BooleanField(
        default=False,
        verbose_name='Скрыто',
    )
    topics = models.ManyToManyField(
        Topic,
        related_name='videos',
        blank=True,
        verbose_name='Темы',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.title

    @property
    def likes_count(self) -> int:
        """Возвращает количество лайков"""
        return self.ratings.filter(rating_type='like').count()

    @property
    def dislikes_count(self) -> int:
        """Возвращает количество дизлайков"""
        return self.ratings.filter(rating_type='dislike').count()


class VideoRating(models.Model):
    """Модель для хранения оценок пользователей (лайки/дизлайки)"""
    RATING_CHOICES = [
        ('like', 'Лайк'),
        ('dislike', 'Дизлайк'),
    ]

    video = models.ForeignKey(
        Video,
        on_delete=models.CASCADE,
        related_name='ratings',
        verbose_name='Видео'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    rating_type = models.CharField(
        max_length=10,
        choices=RATING_CHOICES,
        verbose_name='Тип оценки'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = 'Оценка видео'
        verbose_name_plural = 'Оценки видео'
        unique_together = [['video', 'user']]

    def __str__(self) -> str:
        return (
            f'{self.video.title} - {self.rating_type} '
            f'от {self.user.username}'
        )
