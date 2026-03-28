import pytest
from unittest.mock import patch, MagicMock
from io import StringIO
from src.main import main


@pytest.fixture
def mock_input():
    """Фикстура для мокинга ввода пользователя"""
    with patch("builtins.input", return_value="8") as mock:
        yield mock


@pytest.fixture
def mock_print():
    """Фикстура для мокинга вывода в консоль"""
    with patch("builtins.print") as mock:
        yield mock


def test_main_exit_immediately(mock_input, mock_print):
    """Тест: немедленный выход из программы"""
    mock_input.side_effect = ["8"]

    main()

    # Проверяем, что приветствие и прощание были выведены
    assert any(
        "Привет! Добро пожаловать" in call[0][0] for call in mock_print.call_args_list
    )
    assert any("До свидания!" in call[0][0] for call in mock_print.call_args_list)


def test_main_load_json_success(mock_input, mock_print):
    """Тест: успешная загрузка JSON-файла"""
    # Мокаем открытие файла и его содержимое
    json_content = """[
        {"date": "2023-01-01", "description": "Покупка", "amount": 1000, "currency": "RUB", "status": "EXECUTED"}
    ]"""
    mock_file = MagicMock()
    mock_file.__enter__.return_value = StringIO(json_content)

    with patch("builtins.open", return_value=mock_file):
        mock_input.side_effect = [
            "1",  # Загрузить JSON
            "test.json",  # Путь к файлу
            "8",  # Выход
        ]

        main()

    print_calls = [call[0][0].lower() for call in mock_print.call_args_list]
    assert any("загружено 1 транзакций" in msg for msg in print_calls)


def test_main_load_json_file_not_found(mock_input, mock_print):
    """Тест: ошибка загрузки JSON — файл не найден"""
    with patch("builtins.open", side_effect=FileNotFoundError("File not found")):
        mock_input.side_effect = ["1", "nonexistent.json", "8"]

        main()

    print_calls = [call[0][0].lower() for call in mock_print.call_args_list]
    assert any("ошибка загрузки json-файла" in msg for msg in print_calls)


def test_main_search_transactions_found(mock_input, mock_print):
    """Тест: поиск транзакций — совпадения найдены"""
    # Подготавливаем данные с двумя транзакциями
    json_content = """[
        {"date": "2023-01-01", "description": "Покупка продуктов", "amount": 500, "currency": "RUB", "status": "EXECUTED"},
        {"date": "2023-01-02", "description": "Оплата кафе", "amount": 800, "currency": "RUB", "status": "EXECUTED"}
    ]"""
    mock_file = MagicMock()
    mock_file.__enter__.return_value = StringIO(json_content)

    with patch("builtins.open", return_value=mock_file):
        mock_input.side_effect = [
            "1",
            "test.json",  # Загрузка данных
            "2",
            "Покупка",  # Поиск по слову "Покупка"
            "8",  # Выход
        ]

        main()

    print_output = "\n".join(call[0][0] for call in mock_print.call_args_list)
    assert "Найдено 1 транзакций:" in print_output
    assert "01.01.2023 Покупка продуктов" in print_output


def test_main_search_transactions_not_found(mock_input, mock_print):
    """Тест: поиск транзакций — совпадений нет"""
    json_content = """[
        {"id": 1, "description": "Оплата интернета", "amount": 1000, "category": "Коммунальные услуги"},
        {"id": 2, "description": "Покупка продуктов", "amount": 3000, "category": "Продукты"}
    ]"""
    mock_file = MagicMock()
    mock_file.__enter__.return_value = StringIO(json_content)

    with patch("builtins.open", return_value=mock_file):
        mock_input.side_effect = [
            "1",
            "test.json",  # Загрузка данных
            "2",
            "Неизвестная операция",  # Поиск с отсутствием совпадений
            "8",  # Выход
        ]

        main()

    print_output = "\n".join(call[0][0] for call in mock_print.call_args_list)
    assert "Найдено 0 транзакций:" in print_output


def test_main_count_categories(mock_input, mock_print):
    """Тест: подсчёт транзакций по категориям"""
    json_content = """[
        {"description": "Продукты в магазине"},
        {"description": "Обед в кафе"},
        {"description": "Бензин на заправке"}
    ]"""
    mock_file = MagicMock()
    mock_file.__enter__.return_value = StringIO(json_content)

    with patch("builtins.open", return_value=mock_file):
        mock_input.side_effect = [
            "1",
            "test.json",
            "3",
            "продукты, кафе, транспорт",
            "8",
        ]

        main()

    print_output = "\n".join(call[0][0].lower() for call in mock_print.call_args_list)
    assert "продукты: 1 операций" in print_output
    assert "кафе: 1 операций" in print_output
    assert "транспорт: 0 операций" in print_output


def test_main_filter_by_status_valid(mock_input, mock_print):
    """Тест: фильтрация по корректному статусу"""
    json_content = """[
        {"status": "EXECUTED", "description": "Успешная операция"}
    ]"""
    mock_file = MagicMock()
    mock_file.__enter__.return_value = StringIO(json_content)

    with patch("builtins.open", return_value=mock_file):
        mock_input.side_effect = [
            "1",
            "test.json",
            "4",
            "EXECUTED",
            "7",  # Показать транзакции
            "8",
        ]

        main()

    print_output = "\n".join(call[0][0] for call in mock_print.call_args_list)
    assert 'Операции отфильтрованы по статусу "EXECUTED"' in print_output


def test_main_no_data_operations(mock_input, mock_print):
    """Тест: операции без загруженных данных"""
    mock_input.side_effect = [
        "2",  # Поиск без данных
        "3",  # Подсчёт категорий без данных
        "8",  # Выход
    ]

    main()

    print_output = "\n".join(call[0][0] for call in mock_print.call_args_list)
    count = print_output.count("Сначала загрузите данные")
    assert count == 2


def test_main_invalid_choice(mock_input, mock_print):
    """Тест: неверный выбор пункта меню"""
    mock_input.side_effect = ["999", "8"]  # Неверный пункт  # Выход

    main()

    print_output = "\n".join(call[0][0] for call in mock_print.call_args_list)
    assert "Неверный выбор. Попробуйте снова." in print_output
