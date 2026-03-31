from datetime import datetime
from typing import Any, Dict, List, Optional

AVAILABLE_STATUSES = ["EXECUTED", "PENDING", "FAILED"]


def filter_by_status(
    data: List[Dict[str, Any]], status: str
) -> Optional[List[Dict[str, Any]]]:
    """Фильтрация транзакций по статусу."""
    if status.upper() not in AVAILABLE_STATUSES:
        return None
    filtered = [t for t in data if t.get("state", "").upper() == status.upper()]
    return filtered


def sort_by_date(
    data: List[Dict[str, Any]], ascending: bool = True
) -> List[Dict[str, Any]]:
    """Сортировка транзакций по дате."""

    def parse_date(date_str: str) -> datetime:
        """Парсинг строки даты в объект datetime."""
        try:
            # Пробуем разные форматы дат
            for fmt in (
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%d",
                "%d.%m.%Y %H:%M:%S",
                "%d.%m.%Y",
            ):
                try:
                    return datetime.strptime(date_str, fmt)
                except (ValueError):
                    continue
            # Если ни один формат не подошёл, возвращаем минимальную дату
            return datetime.min
        except (TypeError, ValueError):
            return datetime.min

    sorted_data = sorted(
        data, key=lambda x: parse_date(x.get("date", "")), reverse=not ascending
    )
    return sorted_data


def search_transactions_by_description(
    data: List[Dict[str, Any]], pattern: str
) -> List[Dict[str, Any]]:
    """Поиск транзакций по описанию (регулярные выражения)."""
    import re

    results = []
    for transaction in data:
        description = transaction.get("description", "").lower()
        if re.search(pattern.lower(), description):
            results.append(transaction)
    return results


def count_transactions_by_categories(
    data: List[Dict[str, Any]], categories: List[str]
) -> Dict[str, int]:
    """Подсчёт транзакций по категориям."""
    counts = {category: 0 for category in categories}
    for transaction in data:
        # Сначала пробуем получить категорию напрямую
        category = transaction.get("category", "").lower()
        if not category:
            # Если категории нет, используем описание для поиска совпадений
            category = transaction.get("description", "").lower()

        for cat in categories:
            if cat.lower() in category:
                counts[cat] += 1
    return counts


def filter_ruble_transactions(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Фильтрация рублёвых транзакций."""
    ruble_currencies = ["руб", "rur", "rub", "рубли"]
    filtered = []
    for transaction in data:
        currency = str(transaction.get("currency", "")).lower()
        if any(rub in currency for rub in ruble_currencies):
            filtered.append(transaction)
    return filtered


def format_transaction(transaction: Dict[str, Any]) -> str:
    """Форматирование транзакции для вывода."""
    parts = []
    for key, value in transaction.items():
        parts.append(f"{key}: {value}")
    return "\n".join(parts)
