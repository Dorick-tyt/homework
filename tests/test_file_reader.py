import unittest
from unittest.mock import patch
import pandas as pd
from src.file_reader import load_csv_transactions, load_excel_transactions


class TestLoadFinancialTransactions(unittest.TestCase):

    @patch("os.path.exists", return_value=False)
    def test_file_not_found(self, _):
        """Тест обработки отсутствующего файла."""
        result = load_csv_transactions("nonexistent.csv")
        self.assertIsNone(result)

    @patch("builtins.open", side_effect=IOError("Permission denied"))
    @patch("os.path.exists", return_value=True)
    def test_io_error(self, _, __):
        """Тест обработки ошибки ввода-вывода."""
        result = load_csv_transactions("test.csv")
        self.assertIsNone(result)


class TestLoadExcelTransactions(unittest.TestCase):

    @patch("pandas.read_excel")
    @patch("os.path.exists", return_value=True)
    def test_load_excel_success(self, _, mock_read_excel):
        """Тест успешной загрузки Excel-файла."""
        # Создаём тестовый DataFrame
        test_df = pd.DataFrame(
            {
                "date": ["2024-01-01", "2024-01-02"],
                "amount": [100.0, 50.0],
                "description": ["Salary", "Groceries"],
            }
        )
        mock_read_excel.return_value = test_df

        result = load_excel_transactions("test.xlsx")

        self.assertIsNotNone(result)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["date"], "2024-01-01")
        self.assertEqual(result[0]["amount"], 100.0)
        self.assertEqual(result[1]["description"], "Groceries")

    @patch("os.path.exists", return_value=False)
    def test_excel_file_not_found(self, _):
        """Тест обработки отсутствующего Excel-файла."""
        result = load_excel_transactions("nonexistent.xlsx")
        self.assertIsNone(result)

    @patch("pandas.read_excel", side_effect=Exception("Excel read error"))
    @patch("os.path.exists", return_value=True)
    def test_excel_read_error(self, _, __):
        """Тест обработки ошибки чтения Excel-файла."""
        result = load_excel_transactions("test.xlsx")
        self.assertIsNone(result)

    @patch("pandas.read_excel")
    @patch("os.path.exists", return_value=True)
    def test_custom_sheet_name(self, _, mock_read_excel):
        """Тест загрузки с указанием конкретного листа."""
        test_df = pd.DataFrame({"col1": ["a", "b"], "col2": [1, 2]})
        mock_read_excel.return_value = test_df

        result = load_excel_transactions("test.xlsx", sheet_name="CustomSheet")

        self.assertIsNotNone(result)
        self.assertEqual(len(result), 2)
        mock_read_excel.assert_called_with("test.xlsx", sheet_name="CustomSheet")

    @patch("pandas.read_excel")
    @patch("os.path.exists", return_value=True)
    def test_empty_excel(self, _, mock_read_excel):
        """Тест загрузки пустого Excel-файла."""
        empty_df = pd.DataFrame()
        mock_read_excel.return_value = empty_df

        result = load_excel_transactions("empty.xlsx")
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 0)
