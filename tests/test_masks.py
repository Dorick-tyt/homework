import unittest
from unittest.mock import MagicMock, patch

from src.masks import mask_account_number, mask_card_number


class TestMasks(unittest.TestCase):

    def setUp(self):
        """Инициализация перед каждым тестом."""
        # Создаём мок логгера
        self.mock_logger = MagicMock()
        # Подменяем логгер в модуле masks
        patcher = patch("src.masks.logger", self.mock_logger)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_mask_card_number_success(self):
        """Тест успешной маскировки номера карты."""
        result = mask_card_number("1234 5678 9012 3456")
        self.assertEqual(result, "123456******3456")
        self.mock_logger.debug.assert_called_once_with(
            "Попытка замаскировать номер карты: 1234 5678 9012 3456"
        )
        self.mock_logger.info.assert_called_once_with(
            "Номер карты успешно замаскирован: 123456******3456"
        )

    def test_mask_card_number_with_spaces_and_dashes(self):
        """Тест маскировки карты с пробелами и дефисами."""
        result = mask_card_number("1234-5678-9012-3456")
        self.assertEqual(result, "123456******3456")
        self.mock_logger.debug.assert_called_with(
            "Попытка замаскировать номер карты: 1234-5678-9012-3456"
        )

    def test_mask_card_number_non_digit_characters(self):
        """Тест с нечисловыми символами в номере карты."""
        with self.assertRaises(ValueError) as context:
            mask_card_number("1234abcd5678efgh")
        self.assertIn(
            "Номер карты должен содержать не менее 16 цифр", str(context.exception)
        )
        self.mock_logger.error.assert_called_once_with(
            "Некорректная длина номера карты: 8 цифр"
        )

    def test_mask_card_number_empty_string(self):
        """Тест с пустой строкой."""
        with self.assertRaises(ValueError) as context:
            mask_card_number("")
        self.assertIn(
            "Номер карты должен содержать не менее 16 цифр", str(context.exception)
        )
        self.mock_logger.error.assert_called_once_with(
            "Некорректная длина номера карты: 0 цифр"
        )

    def test_mask_card_number_invalid_length(self):
        """Тест с номером карты неправильной длины (не 16 цифр)."""
        with self.assertRaises(ValueError) as context:
            mask_card_number("12345678")
        self.assertIn(
            "Номер карты должен содержать не менее 16 цифр", str(context.exception)
        )
        self.mock_logger.error.assert_called_once_with(
            "Некорректная длина номера карты: 8 цифр"
        )

    def test_mask_card_number_single_digit(self):
        """Тест с одноцифровым номером карты."""
        with self.assertRaises(ValueError) as context:
            mask_card_number("5")
        self.assertIn(
            "Номер карты должен содержать не менее 16 цифр", str(context.exception)
        )
        self.mock_logger.error.assert_called_once_with(
            "Некорректная длина номера карты: 1 цифр"
        )

    def test_mask_account_number_success(self):
        """Тест успешной маскировки номера счёта."""
        result = mask_account_number("40817810099910004312")
        self.assertEqual(result, "**4312")
        self.mock_logger.debug.assert_called_once_with(
            "Попытка замаскировать номер счёта: 40817810099910004312"
        )
        self.mock_logger.info.assert_called_once_with(
            "Номер счёта успешно замаскирован: **4312"
        )

    def test_mask_account_number_with_non_digits(self):
        """Тест маскировки счёта с нечисловыми символами."""
        result = mask_account_number("4081-7810-0999-1000-4312")
        self.assertEqual(result, "**4312")
        self.mock_logger.debug.assert_called_with(
            "Попытка замаскировать номер счёта: 4081-7810-0999-1000-4312"
        )

    def test_mask_account_number_too_short(self):
        """Тест с слишком коротким номером счёта (меньше 4 цифр)."""
        with self.assertRaises(ValueError) as context:
            mask_account_number("123")
        self.assertIn(
            "Номер счёта должен содержать минимум 4 цифры", str(context.exception)
        )
        self.mock_logger.error.assert_called_once_with(
            "Слишком короткий номер счёта: 3 цифр"
        )

    def test_mask_account_number_minimum_length(self):
        """Тест номера счёта минимальной длины (4 цифры)."""
        result = mask_account_number("1234")
        self.assertEqual(result, "**1234")
        self.mock_logger.info.assert_called_once_with(
            "Номер счёта успешно замаскирован: **1234"
        )
