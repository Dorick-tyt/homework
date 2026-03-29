from typing import Dict, Any
from src.data_loader import load_financial_transactions
from src.filters import process_bank_search
from src.masks import mask_card_number, mask_account_number
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


def get_status_filter() -> str:
    """Запрашивает у пользователя статус для фильтрации."""
    while True:
        status = input("Пользователь: ").upper()
        if status in AVAILABLE_STATUSES:
            return status
        else:
            print(f'Программа: Статус операции "{status}" недоступен.')
            print(
                "Программа: Введите статус, по которому необходимо выполнить фильтрацию."
            )
            print(f"Доступные для фильтровки статусы: {', '.join(AVAILABLE_STATUSES)}")


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


def format_transaction(transaction: Dict[str, Any]) -> str:
    """Форматирует транзакцию для вывода в консоль с маскировкой данных."""
    date_str = transaction.get("date", "")
    description = transaction.get("description", "")

    # Извлекаем и маскируем информацию о счетах/картах
    from_account = transaction.get("from", "")
    to_account = transaction.get("to", "")

    # Маскируем номера карт и счетов
    if from_account and "card" in from_account.lower():
        from_account = mask_card_number(from_account)
    elif (
        from_account
        and "account" in from_account.lower()
        or "счёт" in from_account.lower()
    ):
        from_account = mask_account_number(from_account)

    if to_account and "card" in to_account.lower():
        to_account = mask_card_number(to_account)
    elif to_account and "account" in to_account.lower() or "счёт" in to_account.lower():
        to_account = mask_account_number(to_account)

    # Форматируем сумму
    amount_info = transaction.get("amount", {})
    amount = amount_info.get("value", "N/A")
    currency = amount_info.get("currency", "").upper()

    lines = [f"{date_str} {description}"]

    if from_account:
        lines.append(from_account)
    if to_account:
        if from_account:  # Если есть отправитель, добавляем стрелку
            lines.append(f"-> {to_account}")
        else:
            lines.append(to_account)

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
    status = get_status_filter()

    filtered_data = filter_by_status(data, status)
    if filtered_data is None:
        # Если статус не найден, возвращаем к вводу
        print(f'Программа: Статус операции "{status}" недоступен.')
        print("Программа: Введите статус, по которому необходимо выполнить фильтрацию.")
        print(f"Доступные для фильтровки статусы: {', '.join(AVAILABLE_STATUSES)}")
        status = get_status_filter()
        filtered_data = filter_by_status(data, status)

    if filtered_data is None or len(filtered_data) == 0:
        print("Программа: Не найдено ни одной транзакции с указанным статусом.")
        return

    print(f'Программа: Операции отфильтрованы по статусу "{status}"')

    # Сортировка по дате — проверяем, что filtered_data не None
    if get_yes_no_input("Программа: Отсортировать операции по дате? Да/Нет\n"):
        ascending_input = (
            input(
                "Программа: Отсортировать по возрастанию или по убыванию?\nПользователь: "
            )
            .lower()
            .strip()
        )
        ascending = ascending_input in ["по возрастанию", "возрастание", "asc", "a"]
        if filtered_data is not None:
            filtered_data = sort_by_date(filtered_data, ascending=ascending)

    # Фильтрация рублёвых транзакций — проверяем, что filtered_data не None
    if get_yes_no_input("Программа: Выводить только рублёвые транзакции? Да/Нет\n"):
        if filtered_data is not None:
            filtered_data = filter_ruble_transactions(filtered_data)

    # Поиск по описанию — проверяем, что filtered_data не None
    if get_yes_no_input(
        "Программа: Отфильтровать список транзакций по определённому слову в описании? Да/Нет\n"
    ):
        search_term = input("Программа: Введите строку для поиска: ")
        if filtered_data is not None:
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
