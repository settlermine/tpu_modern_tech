from django.contrib import admin

from .models import UserActionLog


@admin.register(UserActionLog)
class UserActionLogAdmin(admin.ModelAdmin):
    """Административная панель для модели UserActionLog"""
    list_display = [
        'timestamp',
        'user',
        'action',
    ]
    list_filter = [
        'timestamp',
        'user',
    ]
    search_fields = [
        'action',
        'user__username',
    ]
    readonly_fields = [
        'user',
        'action',
        'timestamp',
    ]
    list_per_page = 50

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
