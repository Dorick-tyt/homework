import unittest
from src.processing import (
    filter_by_status,
    sort_by_date,
    search_transactions_by_description,
    count_transactions_by_categories,
    filter_ruble_transactions,
)


class TestProcessing(unittest.TestCase):

    def setUp(self):
        """Подготовка тестовых данных."""
        self.test_data = [
            {
                "id": 1,
                "date": "2024-01-01 10:00:00",
                "amount": 1000,
                "description": "Salary payment",
                "status": "EXECUTED",
                "currency": "RUB",
            },
            {
                "id": 2,
                "date": "2024-01-02 11:30:00",
                "amount": 500,
                "description": "Groceries shopping",
                "status": "PENDING",
                "currency": "USD",
            },
            {
                "id": 3,
                "date": "2024-01-03 09:15:00",
                "amount": 200,
                "description": "Coffee with friends",
                "status": "EXECUTED",
                "currency": "руб",
            },
        ]

    def test_filter_by_status_invalid(self):
        """Тест фильтрации по невалидному статусу."""
        result = filter_by_status(self.test_data, "INVALID_STATUS")
        self.assertIsNone(result)

    def test_sort_by_date_ascending(self):
        """Тест сортировки по дате (возрастание)."""
        result = sort_by_date(self.test_data, ascending=True)
        dates = [t["date"] for t in result]
        self.assertEqual(dates, sorted(dates))

    def test_sort_by_date_descending(self):
        """Тест сортировки по дате (убывание)."""
        result = sort_by_date(self.test_data, ascending=False)
        dates = [t["date"] for t in result]
        self.assertEqual(dates, sorted(dates, reverse=True))

    def test_search_transactions_by_description_match(self):
        """Тест поиска транзакций по описанию (совпадение)."""
        result = search_transactions_by_description(self.test_data, "Groceries")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["description"], "Groceries shopping")

    def test_search_transactions_by_description_regex(self):
        """Тест поиска с использованием регулярных выражений."""
        result = search_transactions_by_description(self.test_data, r"Coffee.*friends")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["description"], "Coffee with friends")

    def test_search_transactions_by_description_no_match(self):
        """Тест поиска без совпадений."""
        result = search_transactions_by_description(self.test_data, "Nonexistent")
        self.assertEqual(len(result), 0)

    def test_count_transactions_by_categories(self):
        """Тест подсчёта транзакций по категориям."""
        categories = ["Groceries", "Coffee", "Salary"]
        result = count_transactions_by_categories(self.test_data, categories)
        self.assertEqual(result["Groceries"], 1)
        self.assertEqual(result["Coffee"], 1)
        self.assertEqual(result["Salary"], 1)

    def test_filter_ruble_transactions(self):
        """Тест фильтрации рублёвых транзакций."""
        result = filter_ruble_transactions(self.test_data)
        self.assertEqual(len(result), 2)
