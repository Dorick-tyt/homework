import logging

logging.disable(logging.INFO)


import os
import pandas as pd
import json
from typing import Any, Dict, List, Optional
from datetime import datetime
from src.filters import process_bank_search
from src.masks import mask_card_number
from src.processing import (
    filter_by_status,
    sort_by_date,
)

AVAILABLE_STATUSES = ["EXECUTED", "CANCELED", "PENDING"]


def get_user_choice() -> int:
    """Получает выбор пользователя из меню."""
    while True:
        try:
            choice = int(input("Пользователь: "))
            if choice in [1, 2, 3]:
                return choice
            else:
                print("Программа: Неверный выбор. Пожалуйста, выберите 1, 2 или 3.")
        except (ValueError):
            print("Программа: Пожалуйста, введите число 1, 2 или 3.")


def get_status_input() -> str:
    """Запрашивает у пользователя статус для фильтрации."""
    while True:
        status = input("Пользователь: ").upper().strip()
        if status in AVAILABLE_STATUSES:
            return status
        else:
            print(
                f"Программа: Неверный статус. Доступные статусы: {', '.join(AVAILABLE_STATUSES)}"
            )


def filter_by_status(
    data: List[Dict[str, Any]], status: str
) -> Optional[List[Dict[str, Any]]]:
    """Фильтрация транзакций по статусу."""
    if status.upper() not in AVAILABLE_STATUSES:
        return None

    filtered = []
    for t in data:
        state_value = t.get("state", "")

        # Проверяем тип и значение
        if isinstance(state_value, str) and state_value:
            if state_value.upper() == status.upper():
                filtered.append(t)
            # Для других типов, которые могут быть строками
        elif state_value is not None:
            try:
                # Пропускаем pandas объекты
                if hasattr(state_value, "shape") or hasattr(state_value, "iloc"):
                    continue
                # Проверяем на NaN
                if pd.isna(state_value):
                    continue
                # Преобразуем в строку и сравниваем
                if str(state_value).upper() == status.upper():
                    filtered.append(t)
            except (TypeError, ValueError):
                continue

    return filtered


def get_yes_no_input(prompt: str) -> bool:
    """Получает от пользователя ответ 'да'/'нет'."""
    while True:
        response = input(f"{prompt}").lower().strip()
        if response in ["да", "д", "yes", "y"]:
            return True
        elif response in ["нет", "н", "no", "n"]:
            return False
        else:
            print("Программа: Пожалуйста, ответьте 'да' или 'нет'.")


def load_financial_transactions(
    file_path: str, **kwargs: Any
) -> Optional[List[Dict[str, Any]]]:
    """
    Загружает транзакции из CSV/XLSX/JSON в виде списка словарей.
    """
    result = None

    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл не найден: {file_path}")

        # Загрузка JSON-файла
        if file_path.lower().endswith(".json"):
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    result = data
                else:
                    print("Предупреждение: JSON-файл должен содержать массив объектов")
                    result = []

        # Загрузка CSV-файла
        elif file_path.lower().endswith(".csv"):
            for sep in [";", ",", "\t"]:
                try:
                    default_csv_params: Dict[str, Any] = {
                        "sep": sep,
                        "encoding": "utf-8",
                        "header": 0,
                        "skip_blank_lines": True,
                    }
                    csv_params = {**default_csv_params, **kwargs}
                    df = pd.read_csv(file_path, **csv_params)
                    result = [
                        {str(k): v for k, v in row.items()}
                        for row in df.to_dict("records")
                    ]
                    print(f"CSV загружен (разделитель '{sep}'): {len(result)} записей")
                    break
                except (pd.errors.ParserError, UnicodeDecodeError):
                    continue
            if result is None:
                raise (ValueError)("Не удалось определить разделитель CSV файла")

        # Загрузка Excel-файла (XLS/XLSX)
        elif file_path.lower().endswith((".xlsx", ".xls")):
            default_excel_params: Dict[str, Any] = {"sheet_name": 0}
            excel_params = {**default_excel_params, **kwargs}
            df = pd.read_excel(file_path, **excel_params)
            result = [
                {str(k): v for k, v in row.items()} for row in df.to_dict("records")
            ]
            print(f"Excel загружен: {len(result)} записей")
        else:
            raise ValueError(
                "Формат файла не поддерживается. Используйте JSON, CSV или XLSX."
            )
    except (Exception) as e:
        print(f"Ошибка загрузки {file_path}: {e}")
        return None

    return result


def filter_ruble_transactions_universal(
    transactions: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Универсальная фильтрация рублёвых транзакций."""
    ruble_transactions = []

    for transaction in transactions:
        # Прямая проверка поля currency_code
        currency_code = transaction.get("currency_code", "")
        currency_name = transaction.get("currency_name", "")

        # Проверяем оба поля
        if currency_code and currency_code.upper() == "RUB":
            ruble_transactions.append(transaction)
        elif currency_name and currency_name.upper() in ["RUBLE", "РУБЛЬ", "РУБ"]:
            ruble_transactions.append(transaction)
        else:
            # Если не нашли по прямым полям, пробуем через универсальную функцию
            currency = get_currency_universal(transaction)
            if currency and currency.upper() in ["RUB", "RUR", "RUBLE", "РУБ"]:
                ruble_transactions.append(transaction)

    return ruble_transactions


def get_currency_universal(transaction: Dict[str, Any]) -> Optional[str]:
    """Универсальное получение кода валюты для любого формата."""

    # Вариант 1: вложенная структура (JSON)
    operation_amount = transaction.get("operationAmount")
    if isinstance(operation_amount, dict):
        currency = operation_amount.get("currency")
        if isinstance(currency, dict):
            return currency.get("code")
        elif isinstance(currency, str):
            return currency

    # Вариант 2: плоская структура (CSV/XLSX)
    # Проверяем все возможные названия полей
    for field in ["currency_code", "currency", "Currency", "CURRENCY", "valute_code"]:
        if field in transaction:
            value = transaction[field]
            if value is not None:
                # Пропускаем NaN
                try:
                    if pd.isna(value):
                        continue
                except (TypeError, ValueError):
                    pass

                # Если это строка и не пустая
                if isinstance(value, (int, float)):
                    # Если это число, например 643 для RUB
                    return str(int(value)) if value == int(value) else str(value)
                elif isinstance(value, str):
                    return value
                else:
                    return str(value)

    return None


def get_amount_universal(transaction: Dict[str, Any]) -> Optional[str]:
    """Получение суммы для любого формата."""

    # Вариант 1: вложенная структура (JSON)
    operation_amount = transaction.get("operationAmount")
    if isinstance(operation_amount, dict):
        amount = operation_amount.get("amount")
        if amount is not None:
            return str(amount)

    # Вариант 2: плоская структура (CSV/XLSX)
    # Проверяем все возможные названия полей
    for field in ["amount", "Amount", "AMOUNT", "sum", "Sum"]:
        if field in transaction:
            value = transaction[field]
            # Исправленная проверка
            if value is not None:
                try:
                    if pd.isna(value):
                        continue
                except (TypeError, ValueError):
                    pass

                if isinstance(value, (str, int, float)):
                    if isinstance(value, str) and not value:
                        continue
                    return str(value)

    return None


def format_transaction(transaction: Dict[str, Any]) -> str:
    """Форматирует транзакцию для вывода в консоль с маскировкой данных."""
    # Форматирование даты
    date_iso = transaction.get("date", "")
    try:
        if date_iso and isinstance(date_iso, str):
            # Убираем Z и заменяем на +00:00 для корректного парсинга
            date_iso_clean = date_iso.replace("Z", "+00:00")
            date_obj = datetime.fromisoformat(date_iso_clean)
            date_str = date_obj.strftime("%d.%m.%Y")
        else:
            date_str = "Неизвестная дата"
    except (ValueError, TypeError, AttributeError):
        # Если не удалось распарсить, пробуем взять первые 10 символов
        if isinstance(date_iso, str) and len(date_iso) >= 10:
            date_str = date_iso[:10].replace("-", ".")
        else:
            date_str = "Неизвестная дата"

    description = transaction.get("description", "")

    # Извлекаем и маскируем информацию о счетах/картах
    from_account = transaction.get("from", "")
    to_account = transaction.get("to", "")

    # Маскируем номера карт и счетов
    from_account_masked = mask_card_number(from_account) if from_account else ""
    to_account_masked = mask_card_number(to_account) if to_account else ""

    # Получаем сумму (универсально)
    amount = get_amount_universal(transaction)
    if amount is None or amount == "":
        amount = "N/A"

    # Получаем валюту
    currency = get_currency_universal(transaction)
    if currency is None or currency == "":
        currency = ""

    lines = [f"{date_str} {description}"]

    if from_account_masked:
        lines.append(from_account_masked)
    if to_account_masked:
        if from_account_masked:  # Если есть отправитель, добавляем стрелку
            lines.append(f"-> {to_account_masked}")
        else:
            lines.append(to_account_masked)

    lines.append(f"Сумма: {amount} {currency}")
    return "\n".join(lines)


def main() -> None:
    """Основная функция программы."""
    print(
        "Программа: Привет! Добро пожаловать в программу работы с банковскими транзакциями."
    )
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice_str = input("\nВаш выбор: ").strip()

    if not choice_str.isdigit():
        print("Программа: Пожалуйста, введите число 1, 2 или 3.")
        return

    choice = int(choice_str)
    if choice not in [1, 2, 3]:
        print("Программа: Пожалуйста, выберите 1, 2 или 3.")
        return

    # Определяем тип файла по выбору пользователя
    if choice == 1:
        file_type = "JSON"
        expected_extension = ".json"
    elif choice == 2:
        file_type = "CSV"
        expected_extension = ".csv"
    else:  # choice == 3
        file_type = "XLSX"
        expected_extension = ".xlsx"

    file_path = input(f"Программа: Введите путь к {file_type}-файлу: ")

    # Проверка расширения файла
    if not file_path.lower().endswith(expected_extension):
        print(
            f"Программа: Ожидается {file_type}-файл с расширением {expected_extension}"
        )
        return

    # Загрузка данных
    data = load_financial_transactions(file_path)
    print(f"Программа: Загружено транзакций: {len(data) if data else 0}")
    if data is None or not data:
        print("Программа: Не удалось загрузить данные из файла.")
        return

    print(f"Программа: Для обработки выбран {file_type}-файл.")

    # Фильтрация по статусу
    print("Программа: Введите статус, по которому необходимо выполнить фильтрацию.")
    print(f"Доступные для фильтровки статусы: {', '.join(AVAILABLE_STATUSES)}")
    status = get_status_input()

    filtered_data = filter_by_status(data, status)
    print(
        f"Программа: После фильтрации по статусу '{status}': {len(filtered_data) if filtered_data else 0} транзакций"
    )
    if filtered_data is None or len(filtered_data) == 0:
        print(f'Программа: Не найдено ни одной транзакции с статусом "{status}".')
        return

    print(f'Программа: Операции отфильтрованы по статусу "{status}"')

    # Сортировка по дате
    if get_yes_no_input("Программа: Отсортировать операции по дате? Да/Нет\n"):
        ascending_input = (
            input(
                "Программа: Отсортировать по возрастанию или по убыванию?\nПользователь: "
            )
            .lower()
            .strip()
        )
        ascending = ascending_input in ["по возрастанию", "возрастание", "asc", "a"]
        filtered_data = sort_by_date(filtered_data, ascending=ascending)
        print(f"Программа: После сортировки: {len(filtered_data)} транзакций")

    # Фильтрация рублёвых транзакций
    if get_yes_no_input("Программа: Выводить только рублёвые транзакции? Да/Нет\n"):
        filtered_data = filter_ruble_transactions_universal(filtered_data)
        print(f"Программа: После фильтрации рублей: {len(filtered_data)} транзакций")

    # Поиск по описанию
    if get_yes_no_input(
        "Программа: Отфильтровать список транзакций по определённому слову в описании? Да/Нет\n"
    ):
        search_term = input("Программа: Введите строку для поиска: ")
        filtered_data = process_bank_search(filtered_data, search_term)
        print(f"Программа: После поиска: {len(filtered_data)} транзакций")

    # Вывод результатов
    print("Программа: Распечатываю итоговый список транзакций...")
    if not filtered_data or len(filtered_data) == 0:
        print(
            "Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации"
        )
        return

    print(f"\nВсего банковских операций в выборке: {len(filtered_data)}\n")
    for i, transaction in enumerate(filtered_data, 1):
        try:
            output = format_transaction(transaction)
            if output.strip():
                print(output)
                if i < len(filtered_data):
                    print()
            else:
                print(f"Транзакция {i} не сформировала вывод")
        except (Exception) as e:
            print(f"Ошибка при выводе транзакции {i}: {e}")


if __name__ == "__main__":
    print("Программа запущена")
    main()
    print("Программа завершена")
