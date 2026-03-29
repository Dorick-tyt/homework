import unittest
from unittest.mock import patch, Mock

from src.masks import mask_account_number, mask_card_number, setup_logger, logger


class TestSetupLogger(unittest.TestCase):

    @patch("os.makedirs")
    @patch("logging.getLogger")
    def test_setup_logger_success(self, mock_get_logger, mock_makedirs):
        """Тест успешной инициализации логгера."""
        # Мокируем создание директории и получение логгера
        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger

        result = setup_logger()

        self.assertIsNotNone(result)
        mock_makedirs.assert_called_with("logs", exist_ok=True)
        self.assertEqual(result, mock_logger)

    @patch("os.makedirs", side_effect=PermissionError("Permission denied"))
    def test_setup_logger_permission_error(self, mock_makedirs):
        """Тест обработки ошибки прав доступа при создании директории."""
        with patch("builtins.print") as mock_print:
            result = setup_logger()
            self.assertIsNone(result)
            mock_print.assert_called()


class TestMaskCardNumber(unittest.TestCase):

    @patch.object(logger, "debug")
    @patch.object(logger, "error")
    @patch.object(logger, "info")
    def test_valid_card_number(self, mock_info, mock_error, mock_debug):
        """Тест маскировки корректного номера карты."""
        result = mask_card_number("1234567890123456")

        mock_debug.assert_called_with(
            "Попытка замаскировать номер карты: 1234567890123456"
        )
        mock_error.assert_not_called()
        mock_info.assert_called_with("Номер карты успешно замаскирован: 123456****3456")
        self.assertEqual(result, "123456****3456")

    @patch.object(logger, "debug")
    @patch.object(logger, "error")
    @patch.object(logger, "info")
    def test_card_with_spaces(self, mock_info, mock_error, mock_debug):
        """Тест маскировки номера карты с пробелами."""
        result = mask_card_number("1234 5678 9012 3456")

        mock_debug.assert_called()
        mock_error.assert_not_called()
        self.assertEqual(result, "123456****3456")

    @patch.object(logger, "debug")
    @patch.object(logger, "error")
    @patch.object(logger, "info")
    def test_card_with_dashes(self, mock_info, mock_error, mock_debug):
        """Тест маскировки номера карты с дефисами."""
        result = mask_card_number("1234-5678-9012-3456")

        mock_debug.assert_called()
        mock_error.assert_not_called()
        self.assertEqual(result, "123456****3456")

    @patch.object(logger, "debug")
    @patch.object(logger, "error")
    @patch.object(logger, "info")
    def test_short_card_number(self, mock_info, mock_error, mock_debug):
        """Тест обработки короткого номера карты."""
        result = mask_card_number("123456789012")

        mock_debug.assert_called()
        mock_error.assert_called_with("Некорректная длина номера карты: 12 цифр")
        mock_info.assert_not_called()
        self.assertEqual(result, "Номер карты должен содержать 16 цифр")

    @patch.object(logger, "debug")
    @patch.object(logger, "error")
    @patch.object(logger, "info")
    def test_long_card_number(self, mock_info, mock_error, mock_debug):
        """Тест обработки длинного номера карты."""
        result = mask_card_number("1234567890123456789")

        mock_debug.assert_called()
        mock_error.assert_called_with("Некорректная длина номера карты: 19 цифр")
        mock_info.assert_not_called()
        self.assertEqual(result, "Номер карты должен содержать 16 цифр")

    @patch.object(logger, "debug")
    @patch.object(logger, "error")
    @patch.object(logger, "info")
    def test_empty_card_number(self, mock_info, mock_error, mock_debug):
        """Тест обработки пустого номера карты."""
        result = mask_card_number("")

        mock_debug.assert_called()
        mock_error.assert_called_with("Некорректная длина номера карты: 0 цифр")
        mock_info.assert_not_called()
        self.assertEqual(result, "Номер карты должен содержать 16 цифр")


class TestMaskAccountNumber(unittest.TestCase):

    @patch.object(logger, "debug")
    @patch.object(logger, "error")
    @patch.object(logger, "info")
    def test_valid_account_number(self, mock_info, mock_error, mock_debug):
        """Тест маскировки корректного номера счёта."""
        result = mask_account_number("1234567890")

        mock_debug.assert_called_with("Попытка замаскировать номер счёта: 1234567890")
        mock_error.assert_not_called()
        mock_info.assert_called_with("Номер счёта успешно замаскирован: **7890")
        self.assertEqual(result, "**7890")

    @patch.object(logger, "debug")
    @patch.object(logger, "error")
    @patch.object(logger, "info")
    def test_account_with_spaces(self, mock_info, mock_error, mock_debug):
        """Тест маскировки номера счёта с пробелами."""
        result = mask_account_number("12 34 56 78 90")

        mock_debug.assert_called()
        mock_error.assert_not_called()
        self.assertEqual(result, "**7890")

    @patch.object(logger, "debug")
    @patch.object(logger, "error")
    @patch.object(logger, "info")
    def test_account_with_letters(self, mock_info, mock_error, mock_debug):
        """Тест маскировки номера счёта с буквами."""
        result = mask_account_number("acc1234")

        mock_debug.assert_called()
        mock_error.assert_not_called()
        self.assertEqual(result, "**1234")

    @patch.object(logger, "debug")
    @patch.object(logger, "error")
    @patch.object(logger, "info")
    def test_short_account_number(self, mock_info, mock_error, mock_debug):
        """Тест обработки короткого номера счёта."""
        result = mask_account_number("123")

        mock_debug.assert_called()
        mock_error.assert_called_with("Слишком короткий номер счёта: 3 цифр")
        mock_info.assert_not_called()
        self.assertEqual(result, "Номер счёта должен содержать минимум 4 цифры")
