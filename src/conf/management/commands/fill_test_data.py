from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from videos.models import Video, VideoRating
import random
from typing import Any


class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными'

    def handle(
        self,
        *args: Any,
        **options: Any,
    ) -> None:
        self.stdout.write('Начинаем заполнение тестовыми данными...\n')

        # Очистка старых данных
        self.stdout.write('Очистка старых данных...')
        VideoRating.objects.all().delete()
        Video.objects.all().delete()

        # Удаляем только тестовых пользователей (с префиксом test_)
        test_users = User.objects.filter(username__startswith='test_')
        deleted_users_count = test_users.count()
        test_users.delete()
        self.stdout.write(
            self.style.SUCCESS(
                f'Удалено тестовых пользователей: {deleted_users_count}'
            )
        )
        self.stdout.write(
            self.style.SUCCESS('Удалены все видео и оценки\n')
        )

        # Создание тестовых пользователей
        self.stdout.write('Создание тестовых пользователей...')
        test_users_data = [
            {'username': 'test_user1', 'email': 'test1@example.com'},
            {'username': 'test_user2', 'email': 'test2@example.com'},
            {'username': 'test_user3', 'email': 'test3@example.com'},
            {'username': 'test_user4', 'email': 'test4@example.com'},
        ]

        created_users = []
        for user_data in test_users_data:
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password='testpass123'
            )
            created_users.append(user)
            self.stdout.write(
                self.style.SUCCESS(f'Создан пользователь: {user.username}')
            )

        self.stdout.write('')

        # Создание тестовых видео
        self.stdout.write('Создание тестовых видео...')
        videos_data = [
            {
                'title': 'Экстрасенсы. Битва сильнейших, 2 сезон, 27 выпуск',
                'source_url': (
                    'https://rutube.ru/video/'
                    '9b4a90a00de7aa9684ed372de8b3d33a/'
                ),
                'preview_image_url': (
                    'https://rutube.ru/api/video/'
                    '9b4a90a00de7aa9684ed372de8b3d33a/thumbnail/?redirect=1'
                ),
                'is_hidden': False,
            },
            {
                'title': 'Ставка на любовь, Финал. Часть 2',
                'source_url': (
                    'https://rutube.ru/video/'
                    'c2fcedf36a27c55eb28d1610c18963fe/'
                ),
                'preview_image_url': (
                    'https://rutube.ru/api/video/'
                    'c2fcedf36a27c55eb28d1610c18963fe/thumbnail/?redirect=1'
                ),
                'is_hidden': False,
            },
            {
                'title': 'Выживалити. Змееловы, 1 сезон, 5 выпуск',
                'source_url': (
                    'https://rutube.ru/video/'
                    'fadcc1ad8069a866426975656721df70/'
                ),
                'preview_image_url': (
                    'https://rutube.ru/api/video/'
                    'fadcc1ad8069a866426975656721df70/thumbnail/?redirect=1'
                ),
                'is_hidden': False,
            },
            {
                'title': (
                    'Утро ТНТ, 14 ноября 2025. '
                    'Гость программы — Александр Шепс'
                ),
                'source_url': (
                    'https://rutube.ru/video/'
                    'ddd9a3b13e68f2a8f7e6da1ea56d9325/'
                ),
                'preview_image_url': (
                    'https://rutube.ru/api/video/'
                    'ddd9a3b13e68f2a8f7e6da1ea56d9325/thumbnail/?redirect=1'
                ),
                'is_hidden': False,
            },
            {
                'title': (
                    'Максим Перлин о том, '
                    'как заработать миллионы на рекламе'
                ),
                'source_url': (
                    'https://rutube.ru/video/'
                    '6610e03948e7f64c9e97617db3370dff/'
                ),
                'preview_image_url': (
                    'https://rutube.ru/api/video/'
                    '6610e03948e7f64c9e97617db3370dff/thumbnail/?redirect=1'
                ),
                'is_hidden': False,
            },
            {
                'title': (
                    'Как полностью удалить аккаунт Google пошагово. '
                    'Удалил свой Гугл профиль'
                ),
                'source_url': (
                    'https://rutube.ru/video/'
                    '379a5cdb4897a373384ddb6ac7a947e8/'
                ),
                'preview_image_url': (
                    'https://rutube.ru/api/video/'
                    '379a5cdb4897a373384ddb6ac7a947e8/thumbnail/?redirect=1'
                ),
                'is_hidden': True,
            },
            {
                'title': 'Большие девочки, 3 сезон, 1 выпуск',
                'source_url': (
                    'https://rutube.ru/video/'
                    '92a65261faac5075216d295176ed1e84/'
                ),
                'preview_image_url': (
                    'https://rutube.ru/api/video/'
                    '92a65261faac5075216d295176ed1e84/thumbnail/?redirect=1'
                ),
                'is_hidden': False,
            },
            {
                'title': 'В темноте, 1 выпуск',
                'source_url': (
                    'https://rutube.ru/video/'
                    '08843a23bb668c123eabb5d3dca3e45d/'
                ),
                'preview_image_url': (
                    'https://rutube.ru/api/video/'
                    '08843a23bb668c123eabb5d3dca3e45d/thumbnail/?redirect=1'
                ),
                'is_hidden': False,
            },
            {
                'title': 'Остров сокровищ. Знаки судьбы, выпуск 1',
                'source_url': (
                    'https://rutube.ru/video/'
                    'bc232c33cd7b9bca2ee49d7420545c51/'
                ),
                'preview_image_url': (
                    'https://rutube.ru/api/video/'
                    'bc232c33cd7b9bca2ee49d7420545c51/thumbnail/?redirect=1'
                ),
                'is_hidden': True,
            },
            {
                'title': '«Попутчик». 10 выпуск | Узбекистан',
                'source_url': (
                    'https://rutube.ru/video/'
                    '9a72f3e8be8711bafe5aae75c380af68/'
                ),
                'preview_image_url': (
                    'https://rutube.ru/api/video/'
                    '9a72f3e8be8711bafe5aae75c380af68/thumbnail/?redirect=1'
                ),
                'is_hidden': False,
            },
            {
                'title': 'Ставка на любовь 6 выпуск - Шоу на пятнице',
                'source_url': (
                    'https://rutube.ru/video/'
                    'f6200495b2e7d8c6002a034190267fa9/'
                ),
                'preview_image_url': (
                    'https://rutube.ru/api/video/'
                    'f6200495b2e7d8c6002a034190267fa9/thumbnail/?redirect=1'
                ),
                'is_hidden': False,
            },
            {
                'title': (
                    'Экстрасенсы. Битва сильнейших, '
                    '2 сезон, 26 выпуск'
                ),
                'source_url': (
                    'https://rutube.ru/video/'
                    '7a96eadf8b978b5579e781ed263e59a4/'
                ),
                'preview_image_url': (
                    'https://rutube.ru/api/video/'
                    '7a96eadf8b978b5579e781ed263e59a4/thumbnail/?redirect=1'
                ),
                'is_hidden': False,
            },
            {
                'title': (
                    'Как удалить Касперский. '
                    'Удаляю антивирус Касперский стандартным способом '
                    'в Виндовс'
                ),
                'source_url': (
                    'https://rutube.ru/video/'
                    'ebf0f03368d438f7440ae18e9682754a/'
                ),
                'preview_image_url': (
                    'https://rutube.ru/api/video/'
                    'ebf0f03368d438f7440ae18e9682754a/thumbnail/?redirect=1'
                ),
                'is_hidden': True,
            },
        ]

        created_videos = []
        for video_data in videos_data:
            video = Video.objects.create(
                title=video_data['title'],
                source_url=video_data['source_url'],
                preview_image_url=video_data['preview_image_url'],
                is_hidden=video_data.get('is_hidden', False),
            )
            created_videos.append(video)
            self.stdout.write(
                self.style.SUCCESS(f'Создано видео: {video.title}')
            )

        self.stdout.write('')

        # Создание лайков/дизлайков
        self.stdout.write('Создание лайков и дизлайков...')
        ratings_created = 0

        for video in created_videos:
            # Каждый пользователь оценивает каждое видео
            for user in created_users:
                # Случайно выбираем лайк или дизлайк (70% лайков, 30% дизов)
                rating_type = (
                    'like' if random.random() < 0.7 else 'dislike'
                )

                VideoRating.objects.create(
                    video=video,
                    user=user,
                    rating_type=rating_type
                )
                ratings_created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Создано оценок: {ratings_created}'
            )
        )

        # Итоговая статистика
        self.stdout.write('\n' + '=' * 50)
        self.stdout.write(
            self.style.SUCCESS(
                f'\nГотово! Создано:\n'
                f'  - Пользователей: {len(created_users)}\n'
                f'  - Видео: {len(created_videos)}\n'
                f'  - Оценок: {ratings_created}\n'
            )
        )
