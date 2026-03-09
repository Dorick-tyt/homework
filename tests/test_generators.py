import unittest
from parameterized import parameterized
from src.generators import (
    filter_by_currency,
    transaction_descriptions,
    card_number_generator,
)


class TestFilterByCurrency(unittest.TestCase):

    def setUp(self):
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

    @parameterized.expand(
        [
            # Тест 1: Фильтрация по USD
            ("USD", 1, "USD"),
            # Тест 2: Фильтрация по EUR
            ("EUR", 1, "EUR"),
            # Тест 3: Нет совпадений (RUB)
            ("RUB", 0, None),
            # Тест 4: Пустой список транзакций
            ("USD", 0, None, []),
            # Тест 5: Транзакции без поля operationAmount
            (
                "USD",
                0,
                None,
                [
                    {"id": 1, "description": "Без суммы"},
                    {"id": 2, "description": "Тоже без суммы"},
                ],
            ),
        ]
    )
    def test_filter_by_currency(
        self, currency_code, expected_count, expected_currency, transactions=None
    ):
        """Параметризованный тест фильтрации транзакций по валюте."""
        test_transactions = (
            transactions if transactions is not None else self.transactions
        )

        filtered = list(filter_by_currency(test_transactions, currency_code))
        self.assertEqual(len(filtered), expected_count)

        if expected_count > 0 and expected_currency:
            self.assertEqual(
                filtered[0]["operationAmount"]["currency"]["code"], expected_currency
            )


class TestTransactionDescriptions(unittest.TestCase):

    @parameterized.expand(
        [
            # Тест 1: Нормальный случай — 2 транзакции с описаниями
            (
                [
                    {"description": "Перевод организации"},
                    {"description": "Перевод со счета на счет"},
                ],
                ["Перевод организации", "Перевод со счета на счет"],
            ),
            # Тест 2: Пустой список
            ([], []),
            # Тест 3: Транзакции без описаний
            ([{"id": 1}, {"id": 2}], []),
            # Тест 4: Смешанный случай (есть и нет описаний)
            (
                [
                    {"description": "Первое описание"},
                    {"id": 2},
                    {"description": "Третье описание"},
                ],
                ["Первое описание", "Третье описание"],
            ),
            # Тест 5: Одна транзакция с описанием
            ([{"description": "Одиночное описание"}], ["Одиночное описание"]),
        ]
    )
    def test_transaction_descriptions(self, transactions, expected):
        """Параметризованный тест извлечения описаний транзакций."""
        descriptions = list(transaction_descriptions(transactions))
        self.assertEqual(descriptions, expected)


class TestCardNumberGenerator(unittest.TestCase):

    @parameterized.expand(
        [
            # Тест 1: Небольшой диапазон
            (
                1,
                3,
                ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"],
            ),
            # Тест 2: Один номер
            (42, 42, ["0000 0000 0000 0042"]),
            # Тест 3: Минимальное значение
            (1, 1, ["0000 0000 0000 0001"]),
            # Тест 4: Максимальное значение
            (9999999999999999, 9999999999999999, ["9999 9999 9999 9999"]),
            # Тест 5: start < 1 (должно начаться с 1)
            (-5, 2, ["0000 0000 0000 0001", "0000 0000 0000 0002"]),
            # Тест 6: end > max (должно закончиться на max)
            (
                9999999999999998,
                9999999999999999 + 10,
                ["9999 9999 9999 9998", "9999 9999 9999 9999"],
            ),
            # Тест 7: Большой диапазон (первые 3 элемента)
            (
                9999999999999997,
                9999999999999999,
                ["9999 9999 9999 9997", "9999 9999 9999 9998", "9999 9999 9999 9999"],
            ),
        ]
    )
    def test_card_number_generator(self, start, end, expected):
        """Параметризованный тест генератора номеров карт."""
        cards = list(card_number_generator(start, end))
        self.assertEqual(cards, expected)
