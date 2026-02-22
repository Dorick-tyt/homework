def filter_by_state(data: list[dict], state: str = "EXECUTED") -> list[dict]:
    """
       Функция возвращает новый список словарей, содержащий только те словари, у которых ключ
    state соответствует указанному значению
    """
    return [item for item in data if item.get("state") == state]


def sort_by_date(data: list[dict], reverse: bool = True) -> list[dict]:
    """
    Функция должна возвращать новый список, отсортированный по дате (date)
    """
    return sorted(data, key=lambda x: x["date"], reverse=reverse)
