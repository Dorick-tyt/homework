import json
import unittest
from unittest.mock import mock_open, patch

from src.external_api import convert_to_rubles
from src.utils import load_transactions


class TestUtils(unittest.TestCase):

    @patch("builtins.open", mock_open(read_data="[]"))
    @patch("os.path.exists")
    def test_load_transactions_empty_list(self, mock_exists):
        mock_exists.return_value = True
        result = load_transactions("data/operations.json")
        self.assertEqual(result, [])

    @patch("builtins.open", mock_open(read_data='{"not": "a list"}'))
    @patch("os.path.exists")
    def test_load_transactions_not_a_list(self, mock_exists):
        mock_exists.return_value = True
        result = load_transactions("data/operations.json")
        self.assertEqual(result, [])

    @patch("os.path.exists")
    def test_load_transactions_file_not_found(self, mock_exists):
        mock_exists.return_value = False
        result = load_transactions("nonexistent.json")
        self.assertEqual(result, [])

    @patch("builtins.open", mock_open(read_data=json.dumps([{"id": 1, "amount": 100}])))
    @patch("os.path.exists")
    def test_load_transactions_valid_data(self, mock_exists):
        mock_exists.return_value = True
        result = load_transactions("data/operations.json")
        expected = [{"id": 1, "amount": 100}]
        self.assertEqual(result, expected)

    @patch("builtins.open", mock_open(read_data="invalid json"))
    @patch("os.path.exists")
    def test_load_transactions_invalid_json(self, mock_exists):
        mock_exists.return_value = True
        result = load_transactions("invalid.json")
        self.assertEqual(result, [])

    @patch("builtins.open")
    @patch("os.path.exists")
    def test_load_transactions_io_error(self, mock_exists, mock_file_open):
        mock_exists.return_value = True
        mock_file_open.side_effect = IOError("Permission denied")
        result = load_transactions("restricted.json")
        self.assertEqual(result, [])


class TestExternalAPI(unittest.TestCase):

    @patch("src.external_api.get_exchange_rate")
    def test_convert_to_rubles_usd(self, mock_get_rate):
        mock_get_rate.return_value = 75.0
        transaction = {"amount": "100", "currency": "USD"}
        result = convert_to_rubles(transaction)
        self.assertAlmostEqual(result, 7500.0)
        mock_get_rate.assert_called_with("USD")

    @patch("src.external_api.get_exchange_rate")
    def test_convert_to_rubles_eur(self, mock_get_rate):
        mock_get_rate.return_value = 85.0
        transaction = {"amount": "200", "currency": "EUR"}
        result = convert_to_rubles(transaction)
        self.assertAlmostEqual(result, 17000.0)
        mock_get_rate.assert_called_with("EUR")

    def test_convert_to_rubles_rub(self):
        transaction = {"amount": "3000", "currency": "RUB"}
        result = convert_to_rubles(transaction)
        self.assertEqual(result, 3000.0)

    @patch("src.external_api.get_exchange_rate")
    def test_convert_to_rubles_no_rate(self, mock_get_rate):
        mock_get_rate.return_value = None
        transaction = {"amount": "100", "currency": "USD"}
        with self.assertRaises(ValueError):
            convert_to_rubles(transaction)
        mock_get_rate.assert_called()

    @patch("src.external_api.get_exchange_rate")
    def test_convert_to_rubles_zero_amount(self, mock_get_rate):
        mock_get_rate.return_value = 75.0
        transaction = {"amount": "0", "currency": "USD"}
        result = convert_to_rubles(transaction)
        self.assertEqual(result, 0.0)

    @patch("src.external_api.get_exchange_rate")
    def test_convert_to_rubles_decimal_amount(self, mock_get_rate):
        mock_get_rate.return_value = 75.5
        transaction = {"amount": "15.50", "currency": "USD"}
        result = convert_to_rubles(transaction)
        self.assertAlmostEqual(result, 1170.25)

    @patch("src.external_api.get_exchange_rate")
    def test_convert_to_rubles_negative_amount(self, mock_get_rate):
        mock_get_rate.return_value = 75.0
        transaction = {"amount": "-100", "currency": "USD"}
        result = convert_to_rubles(transaction)
        self.assertEqual(result, -7500.0)

    def test_convert_to_rubles_missing_amount_key(self):
        transaction = {"currency": "USD"}  # отсутствует amount
        with self.assertRaises(ValueError):
            convert_to_rubles(transaction)

    @patch("src.external_api.get_exchange_rate")
    def test_convert_to_rubles_invalid_amount_format(self, mock_get_rate):
        mock_get_rate.return_value = 75.0
        transaction = {"amount": "not_a_number", "currency": "USD"}
        with self.assertRaises(ValueError):
            convert_to_rubles(transaction)

    @patch("src.external_api.get_exchange_rate")
    def test_convert_to_rubles_api_error(self, mock_get_rate):
        mock_get_rate.side_effect = Exception("API Error")
        transaction = {"amount": "100", "currency": "USD"}
        with self.assertRaises(Exception) as context:
            convert_to_rubles(transaction)
        self.assertIn("API Error", str(context.exception))
