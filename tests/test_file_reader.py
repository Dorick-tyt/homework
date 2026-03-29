import unittest
from unittest.mock import patch

import pandas as pd

from src.file_reader import (
    load_csv_transactions,
    load_excel_transactions,
)


class TestFileReader(unittest.TestCase):

    @patch("builtins.open", side_effect=FileNotFoundError("File not found"))
    def test_load_csv_file_not_found(self, mock_open):
        """Тест обработки отсутствующего CSV-файла."""
        result = load_csv_transactions("nonexistent.csv")
        self.assertIsNone(result)

    @patch("builtins.open", side_effect=PermissionError("Permission denied"))
    def test_load_csv_permission_error(self, mock_open):
        """Тест обработки ошибки прав доступа при чтении CSV."""
        result = load_csv_transactions("restricted.csv")
        self.assertIsNone(result)

    @patch("pandas.read_excel")
    def test_load_excel_success(self, mock_read_excel):
        """Тест успешной загрузки Excel-файла."""
        # Создаём тестовый DataFrame
        test_df = pd.DataFrame(
            {
                "id": [1, 2],
                "amount": [100.0, 50.0],
                "description": ["Salary", "Groceries"],
            }
        )
        mock_read_excel.return_value = test_df

        result = load_excel_transactions("test.xlsx")

        self.assertIsNotNone(result)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["amount"], 100.0)
        self.assertEqual(result[1]["description"], "Groceries")

    @patch("pandas.read_excel", side_effect=FileNotFoundError("File not found"))
    def test_load_excel_file_not_found(self, mock_read_excel):
        """Тест обработки отсутствующего Excel-файла."""
        result = load_excel_transactions("nonexistent.xlsx")
        self.assertIsNone(result)

    @patch("pandas.read_excel", side_effect=Exception("Excel read error"))
    def test_load_excel_read_error(self, mock_read_excel):
        """Тест обработки ошибки чтения Excel-файла."""
        result = load_excel_transactions("error.xlsx")
        self.assertIsNone(result)
