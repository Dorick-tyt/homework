def filter_by_currency(transactions, currency_code):
    """функция filter_by_currency, которая принимает на вход
    список словарей, представляющих транзакции.
    """

    for transaction in transactions:
        # Проверяем, что в транзакции есть поле operationAmount и currency, а также код валюты
        if (
            'operationAmount' in transaction
            and 'currency' in transaction['operationAmount']
            and transaction['operationAmount']['currency']['code'] == currency_code
        ):
            yield transaction


def transaction_descriptions(transactions):
    """функция transaction_descriptions, принимает
    список словарей с транзакциями и возвращает описание каждой
    операции по очереди.
    """

    for transaction in transactions:
        if 'description' in transaction:
            yield transaction['description']



def card_number_generator(start, end):
    """функция card_number_generator, который выдает номера банковских
    карт в формате XXXX XXXX XXXX XXXX, где X — цифра номера карты.
    Генератор может сгенерировать номера карт в заданном диапазоне от
    0000 0000 0000 0001 до 9999 9999 9999 9999.
    """

    # Убедимся, что границы корректны
    start = max(1, start)
    end = min(9999999999999999, end)

    for number in range(start, end + 1):
        # Преобразуем число в строку и дополняем нулями слева до 16 символов
        num_str = f"{number:016d}"
        # Форматируем строку в формат XXXX XXXX XXXX XXXX
        formatted_number = f"{num_str[:4]} {num_str[4:8]} {num_str[8:12]} {num_str[12:]}"
        yield formatted_number