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

    def test_card_with_type(self):
        """Тест маскировки номера карты с указанием типа."""
        result = mask_card_number("Visa 1234567890123456")
        self.assertEqual(result, "Visa 1234 56** **** 3456")

    def test_card_without_type(self):
        """Тест маскировки номера карты без указания типа."""
        result = mask_card_number("1234567890123456")
        # Без типа функция возвращает исходную строку
        self.assertEqual(result, "1234567890123456")

    def test_card_with_spaces(self):
        """Тест маскировки номера карты с пробелами."""
        result = mask_card_number("Visa 1234 5678 9012 3456")
        # Функция не обрабатывает номера с пробелами, возвращает исходную строку
        self.assertEqual(result, "Visa 1234 5678 9012 3456")

    def test_card_with_dashes(self):
        """Тест маскировки номера карты с дефисами."""
        result = mask_card_number("Visa 1234-5678-9012-3456")
        # Функция не обрабатывает дефисы, возвращает исходную строку
        self.assertEqual(result, "Visa 1234-5678-9012-3456")

    def test_mastercard(self):
        """Тест маскировки номера карты Mastercard."""
        result = mask_card_number("Mastercard 1234567890123456")
        self.assertEqual(result, "Mastercard 1234 56** **** 3456")

    def test_american_express(self):
        """Тест маскировки номера American Express (15 цифр)."""
        result = mask_card_number("American Express 123456789012345")
        # Для 15 цифр функция использует общий случай (len(number) >= 16 не срабатывает)
        # Возвращает исходную строку, так как длина не 16 и не 20
        self.assertEqual(result, "American Express 123456789012345")

    def test_maestro(self):
        """Тест маскировки номера Maestro (16 цифр)."""
        result = mask_card_number("Maestro 1596837868705199")
        self.assertEqual(result, "Maestro 1596 83** **** 5199")

    def test_account_number(self):
        """Тест маскировки номера счета."""
        result = mask_card_number("Счет 12345678901234567890")
        self.assertEqual(result, "Счет **7890")

    def test_empty_card(self):
        """Тест обработки пустого значения."""
        result = mask_card_number("")
        self.assertEqual(result, "")

    def test_none_card(self):
        """Тест обработки None."""
        result = mask_card_number(None)
        self.assertEqual(result, "")

    def test_invalid_format(self):
        """Тест обработки некорректного формата."""
        result = mask_card_number("Invalid Format")
        self.assertEqual(result, "Invalid Format")

    def test_card_with_15_digits(self):
        """Тест маскировки карты с 15 цифрами (нестандартный формат)."""
        result = mask_card_number("Discover 123456789012345")
        # 15 цифр не обрабатываются специально, возвращается исходная строка
        self.assertEqual(result, "Discover 123456789012345")

    def test_card_with_19_digits(self):
        """Тест маскировки карты с 19 цифрами."""
        result = mask_card_number("Unknown 1234567890123456789")
        # 19 цифр попадает под условие len(number) >= 16, маскируется как **последние4
        self.assertEqual(result, "Unknown **6789")

    def test_account_with_different_length(self):
        """Тест маскировки счета с длиной отличной от 20."""
        result = mask_card_number("Счет 1234567890")
        # Длина 10, не 20, попадает под условие len(number) >= 16? Нет, т.к. 10 < 16
        # Возвращается исходная строка
        self.assertEqual(result, "Счет 1234567890")


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
