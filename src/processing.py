from datetime import datetime
from typing import Any, Dict, List


def filter_by_state(
    data: list[dict[str, Any]], state: str = "EXECUTED"
) -> List[Dict[str, Any]]:
    """
       Функция возвращает новый список словарей, содержащий только те словари, у которых ключ
    state соответствует указанному значению
    """
    if not isinstance(data, list):
        raise TypeError("Параметр 'data' должен быть списком")

    return [
        item for item in data if isinstance(item, dict) and item.get("state") == state
    ]


def sort_by_date(
    data: list[dict[str, Any]], reverse: bool = True
) -> List[Dict[str, Any]]:
    """
    Функция должна возвращать новый список, отсортированный по дате (date)
    """
    if not isinstance(data, list):
        raise TypeError("Параметр 'data' должен быть списком")

    def parse_date(item: Dict[str, Any]) -> datetime:
        """Парсит дату из строки ISO в объект datetime."""
        date_str = item["date"]
        try:
            return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        except ValueError as e:
            raise ValueError(
                f"Некорректный формат даты '{date_str}' в элементе {item}"
            ) from e

    # Проверяем наличие ключа 'date' и парсим даты
    for item in data:
        if "date" not in item:
            raise KeyError(f"Элемент {item} не содержит ключа 'date'")

    return sorted(data, key=parse_date, reverse=reverse)
