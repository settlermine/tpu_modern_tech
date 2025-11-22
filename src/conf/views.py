from django.contrib.auth.views import (
    LoginView,
    LogoutView,
)
from django.http import (
    HttpRequest,
    HttpResponse,
)

from .logger import log_user_action


class CustomLoginView(LoginView):
    """Кастомная страница входа"""
    template_name = 'login.html'
    redirect_authenticated_user = True

    def get_success_url(self) -> str:
        return '/'

    def form_valid(
        self,
        form,
    ) -> HttpResponse:
        """Обработка успешного входа"""
        response = super().form_valid(form)
        log_user_action(
            self.request.user,
            'Вход в систему',
        )
        return response


class CustomLogoutView(LogoutView):
    """Кастомная страница выхода"""
    next_page = '/'

    def dispatch(
        self,
        request: HttpRequest,
        *args,
        **kwargs,
    ) -> HttpResponse:
        """Обработка выхода"""
        if request.user.is_authenticated:
            log_user_action(
                request.user,
                'Выход из системы',
            )
        return super().dispatch(request, *args, **kwargs)
