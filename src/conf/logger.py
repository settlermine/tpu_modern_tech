import json
from pathlib import Path
from typing import Optional

from django.conf import settings
from django.contrib.auth import get_user_model

from .models import UserActionLog

User = get_user_model()


def log_user_action(
    user: Optional[User],
    action: str,
) -> None:
    """
    Логирует действие пользователя в модель и файл
    """
    log_entry = UserActionLog.objects.create(
        user=user,
        action=action,
    )

    timestamp = log_entry.timestamp

    username = user.username if user else 'Анонимный'
    # Формат с миллисекундами
    timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

    log_formats = settings.LOG_FORMATS
    log_dir = Path(settings.LOG_DIR)

    log_dir.mkdir(parents=True, exist_ok=True)

    today = timestamp.strftime('%Y-%m-%d')

    # Записываем в каждый формат
    for log_format in log_formats:
        if log_format == 'txt':
            _write_text_log(log_dir, today, username, action, timestamp_str)
        elif log_format == 'xml':
            _write_xml_log(log_dir, today, username, action, timestamp_str)
        elif log_format == 'json':
            _write_json_log(log_dir, today, username, action, timestamp_str)


def _write_text_log(
    log_dir: Path,
    today: str,
    username: str,
    action: str,
    timestamp_str: str,
) -> None:
    """Записывает лог в текстовый формат"""
    log_file = log_dir / f'actions_{today}.text'
    log_string = f'[{timestamp_str}] {username}: {action}\n'
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_string)


def _write_xml_log(
    log_dir: Path,
    today: str,
    username: str,
    action: str,
    timestamp_str: str,
) -> None:
    """Записывает лог в XML формат"""
    log_file = log_dir / f'actions_{today}.xml'

    # Если файл не существует, создаем с заголовком
    if not log_file.exists():
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write('<?xml version="1.0" encoding="utf-8"?>\n<actions>\n')
    else:
        # Удаляем закрывающий тег, если он есть
        with open(log_file, 'r+', encoding='utf-8') as f:
            content = f.read()
            # Удаляем закрывающий тег </actions> если он есть
            content = content.rstrip()
            if content.endswith('</actions>'):
                content = content[:-10].rstrip()
            f.seek(0)
            f.truncate()
            f.write(content)

    # Добавляем новую запись и закрывающий тег
    xml_string = (
        f'  <action>\n'
        f'    <timestamp>{timestamp_str}</timestamp>\n'
        f'    <user>{username}</user>\n'
        f'    <action>{action}</action>\n'
        f'  </action>\n'
        f'</actions>\n'
    )
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(xml_string)


def _write_json_log(
    log_dir: Path,
    today: str,
    username: str,
    action: str,
    timestamp_str: str,
) -> None:
    """Записывает лог в JSONL формат"""
    log_file = log_dir / f'actions_{today}.jsonl'
    log_entry = {
        'timestamp': timestamp_str,
        'user': username,
        'action': action,
    }
    log_string = json.dumps(log_entry, ensure_ascii=False) + '\n'
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_string)
