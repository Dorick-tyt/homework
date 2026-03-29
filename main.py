from src.file_reader import load_csv_transactions, load_excel_transactions
from src.processing import (
    search_transactions_by_description,
    count_transactions_by_categories, format_transaction
)

AVAILABLE_STATUSES = ['EXECUTED', 'PENDING', 'FAILED']

def main() -> None:
    """Основная функция программы с расширенной функциональностью."""
    print("Программа: Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    data = []  # Инициализируем данные

    while True:
        print("\nВыберите действие:")
        print("1. Загрузить транзакции из CSV")
        print("2. Загрузить транзакции из Excel")
        print("3. Поиск транзакций по описанию (регулярные выражения)")
        print("4. Подсчёт транзакций по категориям")
        print("5. Фильтрация по статусу")
        print("6. Сортировка по дате")
        print("7. Фильтрация рублёвых транзакций")
        print("8. Показать все транзакции")
        print("9. Выход")

        choice = input("Пользователь: ").strip()

        if choice == "10":
            print("Программа: До свидания!")
            break

        elif choice == "2":
            file_path = input("Программа: Введите путь к CSV‑файлу: ").strip()
            data = load_csv_transactions(file_path)
            if data:
                print(f"Программа: Загружено {len(data)} транзакций")
            else:
                print("Программа: Не удалось загрузить данные")

        elif choice == "3":
            file_path = input("Программа: Введите путь к Excel‑файлу: ").strip()
            data = load_excel_transactions(file_path)
            if data:
                print(f"Программа: Загружено {len(data)} транзакций")
            else:
                print("Программа: Не удалось загрузить данные")

        elif choice == "4":
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

        elif choice == "5":
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

        elif choice == "6":
            if not data:
                print("Программа: Сначала загрузите данные")
                continue
