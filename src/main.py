import json
import re
from collections import Counter
from datetime import datetime
from typing import Any, Dict, List, Optional

# Доступные статусы операций
AVAILABLE_STATUSES = ["EXECUTED", "CANCELED", "PENDING"]


def load_json_data(file_path: str) -> list[Dict[str, Any]]:
    """Загружает данные из JSON-файла"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            else:
                print("Предупреждение: JSON-файл должен содержать массив объектов")
                return []
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Ошибка загрузки JSON-файла: {e}")
        return []


def filter_by_status(
    data: List[Dict[str, Any]], status: str
) -> Optional[List[Dict[str, Any]]]:
    """Фильтрует транзакции по статусу (с приведением к единому регистру)"""
    status_upper = status.upper()
    if status_upper not in AVAILABLE_STATUSES:
        return None

    filtered: List[Dict[str, Any]] = []
    for transaction in data:
        trans_status = transaction.get("status", "").upper()
        if trans_status == status_upper:
            filtered.append(transaction)
    return filtered


def sort_by_date(
    data: list[Dict[str, Any]], ascending: bool = True
) -> list[Dict[str, Any]]:
    """Сортирует транзакции по дате"""

    def parse_date(input_date_str: str) -> Optional[datetime]:
        try:
            for fmt in ("%Y-%m-%d", "%d.%m.%Y", "%Y-%m-%dT%H:%M:%S"):
                try:
                    return datetime.strptime(input_date_str, fmt)
                except ValueError:
                    continue
            return None
        except TypeError, ValueError:
            return None

    valid_dates: List[tuple[datetime, Dict[str, Any]]] = []
    no_date: List[Dict[str, Any]] = []

    for transaction in data:
        date_str = transaction.get("date", "")
        parsed_date = parse_date(date_str)
        if parsed_date:
            valid_dates.append((parsed_date, transaction))
        else:
            no_date.append(transaction)

    sorted_dates = sorted(valid_dates, key=lambda x: x[0], reverse=not ascending)
    sorted_data: List[Dict[str, Any]] = [item[1] for item in sorted_dates] + no_date
    return sorted_data


def filter_ruble_transactions(data: list[Dict[str, Any]]) -> list[Dict[str, Any]]:
    """Оставляет только рублёвые транзакции"""
    ruble_keywords = ["руб", "rub", "р."]
    result = []

    for transaction in data:
        amount_str = str(transaction.get("amount", "")).lower()
        currency = transaction.get("currency", "").lower()

        if (
            any(keyword in amount_str for keyword in ruble_keywords)
            or "rub" in currency
        ):
            result.append(transaction)

    return result


def format_transaction(transaction: dict[str, Any]) -> str:
    """Форматирует транзакцию для вывода в консоль"""
    date_str = transaction.get("date", "N/A")
    description = transaction.get("description", "N/A")
    amount = transaction.get("amount", "N/A")
    currency = transaction.get("currency", "N/A")

    # Извлекаем дату в формате ДД.ММ.ГГГГ
    try:
        date_part = date_str.split("T")[0]
        parsed_date = datetime.strptime(date_part, "%Y-%m-%d")
        formatted_date = parsed_date.strftime("%d.%m.%Y")
    except TypeError, ValueError:
        formatted_date = date_str

    return f"{formatted_date} {description}\nСумма: {amount} {currency}"


def count_transactions_by_categories(
    transactions: List[Dict[str, Any]], categories: List[str]
) -> Dict[str, int]:
    """Подсчитывает количество транзакций по заданным категориям"""
    category_counter = Counter({category: 0 for category in categories})

    for transaction in transactions:
        description = transaction.get("description", "").lower()

        for category in categories:
            pattern = re.compile(category, re.IGNORECASE)
            if pattern.search(description):
                category_counter[category] += 1
                break

    return dict(category_counter)


def search_transactions_by_description(
    transactions: List[Dict[str, Any]],
    search_string: str,  # Исправлено: было searchstring
) -> List[Dict[str, Any]]:
    """Ищет транзакции по строке в описании с использованием регулярных выражений"""
    pattern = re.compile(
        search_string, re.IGNORECASE
    )  # Исправлено: search_string вместо searchstring
    result = []

    for transaction in transactions:
        description = transaction.get("description", "")
        if pattern.search(description):
            result.append(transaction)

    return result


def main() -> None:
    """Основная функция программы с расширенной функциональностью"""
    print(
        "Программа: Привет! Добро пожаловать в программу работы с банковскими транзакциями."
    )
    data = []  # Инициализируем данные

    while True:
        print("\nВыберите действие:")
        print("1. Загрузить транзакции из JSON")
        print("2. Поиск транзакций по описанию (регулярные выражения)")
        print("3. Подсчёт транзакций по категориям")
        print("4. Фильтрация по статусу")
        print("5. Сортировка по дате")
        print("6. Фильтрация рублёвых транзакций")
        print("7. Показать все транзакции")
        print("8. Выход")

        choice = input("Пользователь: ").strip()

        if choice == "8":
            print("Программа: До свидания!")
            break

        elif choice == "1":
            file_path = input("Программа: Введите путь к JSON‑файлу: ").strip()
            data = load_json_data(file_path)
            if data:
                print(f"Программа: Загружено {len(data)} транзакций")
            else:
                print("Программа: Не удалось загрузить данные")

        elif choice == "2":
            if not data:
                print("Программа: Сначала загрузите данные")
                continue
            search_term = input(
                "Программа: Введите строку для поиска (можно использовать регулярные выражения): "
            ).strip()
            results = search_transactions_by_description(data, search_term)
            print(f"Программа: Найдено {len(results)} транзакций:")
            for transaction in results:
                print(format_transaction(transaction))
                print("-" * 40)

        elif choice == "3":
            if not data:
                print("Программа: Сначала загрузите данные")
                continue
            categories_input = input(
                "Программа: Введите категории через запятую (например: продукты, кафе, транспорт): "
            ).strip()
            categories = [cat.strip() for cat in categories_input.split(",")]
            counts = count_transactions_by_categories(data, categories)
            print("Программа: Результаты подсчёта:")
            for category, count in counts.items():
                print(f"{category}: {count} операций")

        elif choice == "4":
            if not data:
                print("Программа: Сначала загрузите данные")
                continue
            while True:
                print(
                    f"Программа: Введите статус, по которому необходимо выполнить фильтрацию."
                )
                print(
                    f"Доступные для фильтровки статусы: {', '.join(AVAILABLE_STATUSES)}"
                )
                user_status = input(
                    "Пользователь: "
                ).strip()  # Переименована переменная
                filtered_data = filter_by_status(data, user_status)
                if filtered_data is None:
                    print(f'Программа: Статус операции "{user_status}" недоступен.')
                else:
                    data = filtered_data
                    print(
                        f'Программа: Операции отфильтрованы по статусу "{user_status.upper()}"'
                    )
                    break

        elif choice == "5":
            if not data:
                print("Программа: Сначала загрузите данные")
                continue
            order = (
                input(
                    "Программа: Отсортировать по возрастанию или по убыванию?\nПользователь: "
                )
                .strip()
                .lower()
            )
            ascending = "возрастанию" in order
            data = sort_by_date(data, ascending)
            print("Программа: Данные отсортированы")

        elif choice == "6":
            if not data:
                print("Программа: Сначала загрузите данные")
                continue
            data = filter_ruble_transactions(data)
            print("Программа: Оставлены только рублёвые транзакции")

        elif choice == "7":
            if not data:
                print("Программа: Нет данных для отображения")
                continue
            print("Программа: Все транзакции:")
            for transaction in data:
                print(format_transaction(transaction))
                print("-" * 40)

        else:
            print("Программа: Неверный выбор. Попробуйте снова.")
