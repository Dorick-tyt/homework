import unittest
from src.filters import process_bank_search, process_bank_operations

class TestFilters(unittest.TestCase):
    def setUp(self):
        """Подготовка тестовых данных"""
        self.test_data = [
            {'id': 1, 'description': 'Покупка в магазине продуктов', 'amount': 1000},
            {'id': 2, 'description': 'Оплата интернета', 'amount': 500},
            {'id': 3, 'description': 'Перевод другу', 'amount': 2000},
            {'id': 4, 'description': 'Покупка электроники', 'amount': 5000},
            {'id': 5, 'description': 'Оплата кафе', 'amount': 800},
        ]

    def test_process_bank_search_exact_match(self):
        """Тест поиска точного совпадения"""
        result = process_bank_search(self.test_data, 'Оплата интернета')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['id'], 2)

    def test_process_bank_search_partial_match(self):
        """Тест частичного совпадения"""
        result = process_bank_search(self.test_data, 'Покупка')
        self.assertEqual(len(result), 2)  # Покупка продуктов и Покупка электроники
        ids = [item['id'] for item in result]
        self.assertIn(1, ids)
        self.assertIn(4, ids)

    def test_process_bank_search_case_insensitive(self):
        """Тест нечувствительности к регистру"""
        result = process_bank_search(self.test_data, 'покупка')
        self.assertEqual(len(result), 2)

    def test_process_bank_search_no_results(self):
        """Тест отсутствия результатов"""
        result = process_bank_search(self.test_data, 'Неизвестный платеж')
        self.assertEqual(len(result), 0)

    def test_process_bank_search_empty_data(self):
        """Тест с пустыми данными"""
        result = process_bank_search([], 'Покупка')
        self.assertEqual(len(result), 0)

    def test_process_bank_operations_basic(self):
        """Базовый тест подсчёта категорий"""
        categories = ['Покупка', 'Оплата']
        result = process_bank_operations(self.test_data, categories)

        self.assertIn('Покупка', result)
        self.assertIn('Оплата', result)
        self.assertEqual(result['Покупка'], 2)
        self.assertEqual(result['Оплата'], 2)

    def test_process_bank_operations_case_insensitive(self):
        """Тест нечувствительности к регистру при подсчёте"""
        categories = ['покупка', 'оплата']
        result = process_bank_operations(self.test_data, categories)

        self.assertEqual(result['покупка'], 2)
        self.assertEqual(result['оплата'], 2)

    def test_process_bank_operations_no_matches(self):
        """Тест категорий без совпадений"""
        categories = ['Зарплата', 'Возврат']
        result = process_bank_operations(self.test_data, categories)

        self.assertEqual(result['Зарплата'], 0)
        self.assertEqual(result['Возврат'], 0)

    def test_process_bank_operations_empty_data(self):
        """Тест подсчёта с пустыми данными"""
        categories = ['Покупка']
        result = process_bank_operations([], categories)
        self.assertEqual(result['Покупка'], 0)