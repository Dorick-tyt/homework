import re
from collections import Counter
from typing import Any
from typing import Counter as CounterType
from typing import Dict, List


def process_bank_search(
    data: List[Dict[str, Any]], search: str
) -> List[Dict[str, Any]]:
    """
    Ищет транзакции, в описании которых есть заданная строка (с использованием регулярных выражений).

    Args:
        data: список словарей с данными о банковских операциях
        search: строка поиска (может содержать регулярные выражения)

    Returns:
        Список словарей, у которых в поле 'description' есть совпадение с поиском
    """
    if not data or not search:
        return []

    # Компилируем регулярное выражение (игнорируем регистр)
    pattern = re.compile(search, re.IGNORECASE)
    result = []

    for transaction in data:
        description = transaction.get("description", "")
        if isinstance(description, str) and pattern.search(description):
            result.append(transaction)

    return result


def process_bank_operations(
    data: List[Dict[str, Any]], categories: List[str]
) -> Dict[str, int]:
    """
    Подсчитывает количество операций в каждой указанной категории с использованием Counter.

    Поиск выполняется по полю 'description'.

    Args:
        data: список словарей с данными о банковских операциях
        categories: список категорий для подсчёта

    Returns:
        Словарь с категориями и количеством операций в каждой
    """
    # Создаём счётчик для категорий
    category_counter: CounterType[str] = Counter()

    # Приводим категории к нижнему регистру для сравнения
    lower_categories = [cat.lower() for cat in categories]

    for transaction in data:
        description = str(transaction.get("description", "")).lower()
        # Проверяем, содержит ли описание какую‑либо из категорий
        for category in lower_categories:
            if category in description:
                category_counter[category] += 1

    # Преобразуем Counter в обычный словарь с оригинальными названиями категорий
    result: Dict[str, int] = {}
    for category in categories:
        result[category] = category_counter.get(category.lower(), 0)

    return result
