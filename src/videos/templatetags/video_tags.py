from django import template

register = template.Library()


@register.filter
def get_item(dictionary: dict, key: int) -> str | None:
    """Получает значение из словаря по ключу"""
    if dictionary is None:
        return None
    return dictionary.get(key)
