import os
from typing import Dict, Optional

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("EXCHANGE_API_KEY")
BASE_URL = "https://api.exchangeratesapi.io/v1/latest"


def get_exchange_rate(
    base_currency: str, target_currency: str = "RUB"
) -> Optional[float]:
    """
    Получает курс обмена валюты через API.

    Args:
        base_currency (str): Базовая валюта (например, USD, EUR).
        target_currency (str): Целевая валюта (по умолчанию RUB).

    Returns:
        Optional[float]: Курс обмена или None в случае ошибки.
    """
    params = {"access_key": API_KEY, "base": base_currency, "symbols": target_currency}

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        return data["rates"][target_currency]
    except requests.RequestException, KeyError:
        return None


def convert_to_rubles(transaction: Dict) -> float:
    """
    Конвертирует сумму транзакции в рубли.

    Args:
        transaction (Dict): Словарь с данными транзакции.

    Returns:
        float: Сумма в рублях.
    """
    amount = float(transaction.get("amount", 0))
    currency = transaction.get("currency", "RUB")

    if currency == "RUB":
        return amount

    rate = get_exchange_rate(currency)
    if rate is not None:
        return amount * rate
    else:
        raise ValueError(f"Не удалось получить курс для валюты {currency}")
