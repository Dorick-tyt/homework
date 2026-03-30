import os
import pandas as pd
import json
from typing import Any, Dict, List, Optional
from datetime import datetime
from src.filters import process_bank_search
from src.widget import mask_account_card
from src.processing import (
    filter_by_status,
    sort_by_date,
    filter_ruble_transactions,
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
        except ValueError:
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
            default_csv_params: Dict[str, Any] = {
                "sep": ",",
                "encoding": "utf-8",
                "header": 0,
                "skip_blank_lines": True,
            }
            csv_params = {**default_csv_params, **kwargs}
            df = pd.read_csv(file_path, **csv_params)
            result = [
                {str(k): v for k, v in row.items()} for row in df.to_dict("records")
            ]
            print(f"CSV загружен: {len(result)} записей")

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
    except Exception as e:
        print(f"Ошибка загрузки {file_path}: {e}")
        return None

    return result


def format_transaction(transaction: Dict[str, Any]) -> str:
    """Форматирует транзакцию для вывода в консоль с маскировкой данных."""
    # Форматирование даты: из ISO в DD.MM.YYYY
    date_iso = transaction.get("date", "")
    try:
        date_obj = datetime.fromisoformat(date_iso.replace("Z", "+00:00"))
        date_str = date_obj.strftime("%d.%m.%Y")
    except (ValueError, TypeError):
        date_str = "Неизвестная дата"

    description = transaction.get("description", "")

    # Извлекаем и маскируем информацию о счетах/картах
    from_account = transaction.get("from", "")
    to_account = transaction.get("to", "")

    # Маскируем номера карт и счетов
    from_account_masked = mask_account_card(from_account)
    to_account_masked = mask_account_card(to_account)

    # Форматируем сумму
    amount_info = transaction.get("amount", {})
    amount = amount_info.get("value", "N/A")
    currency = amount_info.get("currency", "").upper()

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

    choice = get_user_choice()

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
    if data is None or not data:
        print("Программа: Не удалось загрузить данные из файла.")
        return

    print(f"Программа: Для обработки выбран {file_type}-файл.")

    # Фильтрация по статусу
    print("Программа: Введите статус, по которому необходимо выполнить фильтрацию.")
    print(f"Доступные для фильтровки статусы: {', '.join(AVAILABLE_STATUSES)}")
    status = get_status_input()

    filtered_data = filter_by_status(data, status)

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

    # Фильтрация рублёвых транзакций
    if get_yes_no_input("Программа: Выводить только рублёвые транзакции? Да/Нет\n"):
        filtered_data = filter_ruble_transactions(filtered_data)

    # Поиск по описанию
    if get_yes_no_input(
        "Программа: Отфильтровать список транзакций по определённому слову в описании? Да/Нет\n"
    ):
        search_term = input("Программа: Введите строку для поиска: ")
        filtered_data = process_bank_search(filtered_data, search_term)

    # Вывод результатов
    print("Программа: Распечатываю итоговый список транзакций...")
    if not filtered_data or len(filtered_data) == 0:
        print(
            "Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации"
        )
        return

    print(f"\nВсего банковских операций в выборке: {len(filtered_data)}\n")
    for i, transaction in enumerate(filtered_data, 1):
        print(format_transaction(transaction))
        if i < len(filtered_data):
            print()  # Пустая строка между транзакциями
