import unittest
from src.masks import mask_account_number, mask_card_number
from src.widget import get_date


class TestWidgetFunctions(unittest.TestCase):

    def test_get_mask_card_number_valid(self):
        """Тест маскировки корректного номера карты (только цифры)."""
        result = mask_card_number("7000792289606361")
        self.assertEqual(result, "700079****6361")

    def test_get_mask_card_number_non_digits(self):
        """Тест с нечисловыми символами в номере карты."""
        result = mask_card_number("Visa Platinum 7000792289606361")
        self.assertEqual(result, "700079****6361")

    def test_get_mask_account_valid(self):
        """Тест маскировки корректного номера счёта."""
        result = mask_account_number("40817810099910004312")
        self.assertEqual(result, "**4312")

    def test_get_mask_account_non_digits(self):
        """Тест с нечисловыми символами в номере счёта."""
        result = mask_account_number("Счёт 40817810099910004312")
        self.assertEqual(result, "**4312")

    def test_get_mask_account_too_short(self):
        """Тест с слишком коротким номером счёта."""
        result = mask_account_number("123")
        self.assertIn("Номер счёта должен содержать минимум 4 цифры", result)

    def test_get_date_valid_input(self):
        """Тест преобразования даты."""
        result = get_date("2024-03-11T02:26:18.671407")
        self.assertEqual(result, "11.03.2024")
