import re
from typing import Optional

from src.masks import mask_account_number, mask_card_number


def mask_account_card(card_number: str) -> Optional[str]:
    """
    Маскирует номер карты или счёта в строке.
    """
    card_number = card_number.strip()

    number_match = re.search(r"\d+$", card_number)
    if not number_match:
        return None

    full_number = number_match.group()
    type_part = card_number[: number_match.start()].strip()
    if not type_part:
        return None

    is_account = any(keyword in type_part.lower() for keyword in ["счёт", "account"])

    if is_account:
        masked_number = mask_account_number(full_number)
    else:
        masked_number = mask_card_number(full_number)

    # Проверка на ошибку (возвращается строка с ValueError)
    if "должен содержать" in masked_number:
        return None

    return f"{type_part} {masked_number}"


print(mask_account_card("Visa Platinum 7000792289606361"))


def get_date(date_format: str) -> str:
    """
    Принимает на вход строку с датой в формате "2024-03-11T02:26:18.671407"
     и возвращает строку с датой в формате "ДД.ММ.ГГГГ" ("11.03.2024").
    """
    import re

    date_split_list = date_format.split("T")
    formated_date = re.sub(
        r"(\d{4})-(\d{2})-(\d{2})", r"\3.\2.\1", (date_split_list[0])
    )

    return formated_date
