import unittest
import json
import os
import tempfile
from src.data_loader import load_financial_transactions

class TestDataLoader(unittest.TestCase):
    def setUp(self):
        """Создание временных тестовых файлов"""
        # Создаём временный JSON-файл
        self.json_content = [
            {'id': 1, 'description': 'Test JSON', 'amount': 100},
            {'id': 2, 'description': 'Another JSON', 'amount': 200}
        ]
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump(self.json_content, f)
            self.json_file = f.name

        # Создаём временный CSV-файл
        csv_content = "id,description,amount\n1,Test CSV,150\n2,Another CSV,250"
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write(csv_content)
            self.csv_file = f.name

    def tearDown(self):
        """Удаление временных файлов"""
        if os.path.exists(self.json_file):
            os.unlink(self.json_file)
        if os.path.exists(self.csv_file):
            os.unlink(self.csv_file)

    def test_load_json_file(self):
        """Тест загрузки JSON-файла"""
        result = load_financial_transactions(self.json_file)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['description'], 'Test JSON')

    def test_load_csv_file(self):
        """Тест загрузки CSV-файла"""
        result = load_financial_transactions(self.csv_file)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[1]['description'], 'Another CSV')

    def test_file_not_found(self):
        """Тест обработки несуществующего файла"""
        result = load_financial_transactions('nonexistent.json')
        self.assertIsNone(result)

    def test_unsupported_format(self):
        """Тест неподдерживаемого формата файла"""
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as f:
            self.txt_file = f.name

        result = load_financial_transactions(self.txt_file)
        os.unlink(self.txt_file)
        self.assertIsNone(result)