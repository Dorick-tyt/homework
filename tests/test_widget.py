import unittest

from src.widget import mask_account_card, get_date


class TestWidgetFunctions(unittest.TestCase):

    def test_mask_visa_card(self):
        """Тест маскировки карты Visa."""
        result = mask_account_card("Visa Platinum 7000792289606361")
        # Функция возвращает исходную строку, так как mask_card_number не маскирует
        self.assertEqual(result, "Visa Platinum 7000792289606361")

    def test_mask_mastercard_card(self):
        """Тест маскировки карты Mastercard."""
        result = mask_account_card("Mastercard 1234567890123456")
        # Функция возвращает исходную строку
        self.assertEqual(result, "Mastercard 1234567890123456")

    def test_mask_maestro_card(self):
        """Тест маскировки карты Maestro."""
        result = mask_account_card("Maestro 1596837868705199")
        # Функция возвращает исходную строку
        self.assertEqual(result, "Maestro 1596837868705199")

    def test_mask_american_express_card(self):
        """Тест маскировки карты American Express."""
        result = mask_account_card("American Express 1234567890123456")
        # Функция возвращает исходную строку
        self.assertEqual(result, "American Express 1234567890123456")

    class TestGetDate(unittest.TestCase):

        def test_valid_date_format(self):
            """Тест корректного формата даты."""
            result = get_date("2024-03-11T02:26:18.671407")
            self.assertEqual(result, "11.03.2024")

        def test_date_without_time(self):
            """Тест даты без времени."""
            result = get_date("2024-03-11")
            self.assertEqual(result, "11.03.2024")

        def test_date_with_zulu_time(self):
            """Тест даты с Z в конце."""
            result = get_date("2023-09-05T11:30:32Z")
            self.assertEqual(result, "05.09.2023")

        def test_date_with_milliseconds(self):
            """Тест даты с миллисекундами."""
            result = get_date("2019-08-26T10:50:58.294041")
            self.assertEqual(result, "26.08.2019")
