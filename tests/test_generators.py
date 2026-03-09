import unittest
from src.generators import (
    filter_by_currency,
    transaction_descriptions,
    card_number_generator,
)


class TestFunctions(unittest.TestCase):

    def setUp(self):
        """Подготавливаем тестовые данные перед каждым тестом."""
        self.transactions = [
            {
                "id": 939719570,
                "state": "EXECUTED",
                "date": "2018-06-30T02:08:58.425572",
                "operationAmount": {
                    "amount": "9824.07",
                    "currency": {"name": "USD", "code": "USD"},
                },
                "description": "Перевод организации",
                "from": "Счет 75106830613657916952",
                "to": "Счет 11776614605963066702",
            },
            {
                "id": 142264268,
                "state": "EXECUTED",
                "date": "2019-04-04T23:20:05.206878",
                "operationAmount": {
                    "amount": "79114.93",
                    "currency": {"name": "EUR", "code": "EUR"},
                },
                "description": "Перевод со счета на счет",
                "from": "Счет 19708645243227258542",
                "to": "Счет 75651667383060284188",
            },
        ]

    def test_filter_by_currency_usd(self):
        """Тест фильтрации транзакций по валюте USD."""
        usd_transactions = list(filter_by_currency(self.transactions, "USD"))
        self.assertEqual(len(usd_transactions), 1)  # Было 2, стало 1
        self.assertEqual(
            usd_transactions[0]["operationAmount"]["currency"]["code"], "USD"
        )

    def test_filter_by_currency_eur(self):
        """Тест фильтрации транзакций по валюте EUR."""
        eur_transactions = list(filter_by_currency(self.transactions, "EUR"))
        self.assertEqual(len(eur_transactions), 1)
        self.assertEqual(
            eur_transactions[0]["operationAmount"]["currency"]["code"], "EUR"
        )

    def test_filter_by_currency_no_matches(self):
        """Тест фильтрации, когда нет совпадений."""
        rub_transactions = list(filter_by_currency(self.transactions, "RUB"))
        self.assertEqual(len(rub_transactions), 0)

    def test_transaction_descriptions(self):
        """Тест генератора описаний транзакций."""
        descriptions = list(transaction_descriptions(self.transactions))
        expected = [
            "Перевод организации",
            "Перевод со счета на счет",
        ]  # Удален лишний элемент
        self.assertEqual(descriptions, expected)

    def test_transaction_descriptions_empty_list(self):
        """Тест генератора описаний для пустого списка транзакций."""
        empty_descriptions = list(transaction_descriptions([]))
        self.assertEqual(empty_descriptions, [])

    def test_card_number_generator_small_range(self):
        """Тест генератора номеров карт для небольшого диапазона."""
        cards = list(card_number_generator(1, 3))
        expected = ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"]
        self.assertEqual(cards, expected)

    def test_card_number_generator_single_number(self):
        """Тест генератора номеров карт для одного числа."""
        cards = list(card_number_generator(42, 42))
        expected = ["0000 0000 0000 0042"]
        self.assertEqual(cards, expected)

    def test_card_number_generator_boundary_values(self):
        """Тест граничных значений генератора номеров карт."""
        # Тест минимального значения
        min_card = next(card_number_generator(1, 1))
        self.assertEqual(min_card, "0000 0000 0000 0001")

        # Тест максимального значения (ограниченного в функции)
        max_card = next(card_number_generator(9999999999999999, 9999999999999999))
        self.assertEqual(max_card, "9999 9999 9999 9999")

    def test_card_number_generator_out_of_bounds(self):
        """Тест обработки значений за пределами допустимого диапазона."""
        # start < 1
        cards1 = list(card_number_generator(-5, 2))
        expected1 = ["0000 0000 0000 0001", "0000 0000 0000 0002"]
        self.assertEqual(cards1, expected1)

        # end > max
        cards2 = list(card_number_generator(9999999999999998, 9999999999999999 + 10))
        expected2 = ["9999 9999 9999 9998", "9999 9999 9999 9999"]
        self.assertEqual(cards2, expected2)
