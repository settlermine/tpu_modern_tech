from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class UserActionLog(models.Model):
    """Модель для хранения логов действий пользователей"""
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Пользователь',
    )
    action = models.CharField(
        max_length=200,
        verbose_name='Действие',
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время',
    )

    class Meta:
        verbose_name = 'Лог действия пользователя'
        verbose_name_plural = 'Логи действий пользователей'
        ordering = ['-timestamp']

    def __str__(self) -> str:
        user_str = self.user.username if self.user else 'Анонимный'
        return f'{self.action} - {user_str} ({self.timestamp})'
