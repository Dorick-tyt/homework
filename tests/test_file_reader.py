import unittest
from unittest.mock import patch
import pandas as pd
from src.file_reader import load_financial_transactions


class TestLoadFinancialTransactions(unittest.TestCase):

    def setUp(self):
        """Подготовка тестовых данных перед каждым тестом"""
        # Создаём тестовые CSV-данные
        self.csv_content = """date,amount,category
2023-01-01,1000,Salary
2023-01-02,500,Groceries
2023-01-03,200,Transport"""

        # Создаём тестовый DataFrame для сравнения
        self.expected_df = pd.DataFrame(
            {
                "date": ["2023-01-01", "2023-01-02", "2023-01-03"],
                "amount": [1000, 500, 200],
                "category": ["Salary", "Groceries", "Transport"],
            }
        )

    @patch("os.path.exists")
    @patch("pandas.read_csv")
    def test_csv_loading_success(self, mock_read_csv, mock_exists):
        """Тест успешной загрузки CSV-файла"""
        mock_exists.return_value = True  # Файл существует
        mock_read_csv.return_value = self.expected_df
        result = load_financial_transactions("test.csv")
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 3)
        mock_read_csv.assert_called_once()

    @patch("os.path.exists")
    @patch("pandas.read_excel")
    @patch("pandas.read_csv")  # Нужен для корректного порядка патчей
    def test_excel_loading_success(self, mock_read_csv, mock_read_excel, mock_exists):
        """Тест успешной загрузки XLSX-файла"""
        mock_exists.return_value = True
        mock_read_excel.return_value = self.expected_df
        result = load_financial_transactions("test.xlsx")
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 3)
        mock_read_excel.assert_called_once()
        mock_read_csv.assert_not_called()

    @patch("os.path.exists")
    def test_file_not_found(self, mock_exists):
        """Тест обработки отсутствующего файла"""
        mock_exists.return_value = False
        result = load_financial_transactions("nonexistent.csv")
        self.assertIsNone(result)

    @patch("os.path.exists")
    @patch("pandas.read_csv")
    def test_csv_with_custom_params(self, mock_read_csv, mock_exists):
        """Тест загрузки CSV с пользовательскими параметрами"""
        mock_exists.return_value = True
        custom_params = {"sep": ";", "encoding": "cp1251"}
        mock_read_csv.return_value = self.expected_df
        result = load_financial_transactions("test.csv", **custom_params)
        self.assertIsNotNone(result)
        # Проверяем, что параметры были переданы
        call_kwargs = mock_read_csv.call_args[1]
        self.assertEqual(call_kwargs["sep"], ";")
        self.assertEqual(call_kwargs["encoding"], "cp1251")

    @patch("os.path.exists")
    @patch("pandas.read_csv")
    def test_csv_read_error(self, mock_read_csv, mock_exists):
        """Тест обработки ошибки чтения CSV-файла"""
        mock_exists.return_value = True
        mock_read_csv.side_effect = pd.errors.ParserError("Error parsing CSV")
        result = load_financial_transactions("broken.csv")
        self.assertIsNone(result)

    @patch("os.path.exists")
    @patch("pandas.read_excel")
    def test_excel_read_error(self, mock_read_excel, mock_exists):
        """Тест обработки ошибки чтения XLSX-файла"""
        mock_exists.return_value = True
        mock_read_excel.side_effect = ValueError("Invalid Excel file")
        result = load_financial_transactions("broken.xlsx")
        self.assertIsNone(result)

    def test_unsupported_format(self):
        """Тест неподдерживаемого формата файла"""
        result = load_financial_transactions("document.txt")
        self.assertIsNone(result)

    @patch("os.path.exists")
    @patch("pandas.read_csv")
    def test_empty_csv_file(self, mock_read_csv, mock_exists):
        """Тест пустого CSV-файла"""
        mock_exists.return_value = True
        empty_df = pd.DataFrame()
        mock_read_csv.return_value = empty_df
        result = load_financial_transactions("empty.csv")
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 0)

    @patch("os.path.exists")
    @patch("pandas.read_excel")
    def test_excel_with_multiple_sheets(self, mock_read_excel, mock_exists):
        """Тест Excel-файла с несколькими листами"""
        mock_exists.return_value = True
        # Имитируем возврат первого листа (по умолчанию sheet_name=0)
        mock_read_excel.return_value = self.expected_df
        result = load_financial_transactions("multi_sheet.xlsx")
        # Функция должна вернуть первый лист (по умолчанию sheet_name=0)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 3)
