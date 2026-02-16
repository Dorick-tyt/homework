def mask_account_card(card_number):
    """
    Маскирует номер карты или счёта в строке
    """
    # Очищаем строку от лишних пробелов
    card_number.strip()

    # Ищем номер (последовательность цифр в конце строки)
    import re
    number_match = re.search(r'\d+$', card_number)

    if not number_match:
        return None  # Номер не найден

    full_number = number_match.group()
    type_part = card_number[:number_match.start()].strip()

    if not type_part:
        return None  # Нет названия

    # Определяем тип: если есть "Счёт", то это счёт, иначе — карта
    is_account = any(keyword in type_part.lower() for keyword in ['счёт', 'account',])

    # Применяем соответствующую маску
    if is_account:
        masked_number = get_mask_account(full_number)
    else:
        masked_number = get_mask_card_number(full_number)

    # Если маскировка не удалась (некорректный номер), возвращаем None
    if masked_number is None:
        return None

    # Возвращаем исходную строку с замаскированным номером
    return f"{type_part} {masked_number}"
# Вспомогательные функции маскировки (из предыдущих реализаций)
def get_mask_card_number(card_number):
    digits = ''.join(filter(str.isdigit, card_number))
    if len(digits) != 16:
        return None
    return f"{digits[:4]} {digits[4:6]}** **** {digits[-4:]}"

def get_mask_account(account_number):
    digits = ''.join(filter(str.isdigit, account_number))
    if len(digits) < 4:
        return None
    return f"**{digits[-4:]}"

print(mask_account_card("Visa Platinum 7000792289606361"))

def get_date(date_format: str) -> str:
    """
    Принимает на вход строку с датой в формате "2024-03-11T02:26:18.671407"
     и возвращает строку с датой в формате "ДД.ММ.ГГГГ" ("11.03.2024").
    """
    import re
    date_split_list = date_format.split('T')
    formated_date = re.sub(r"(\d{4})-(\d{2})-(\d{2})", r"\3.\2.\1", (date_split_list[0]))

    return formated_date

print (get_date("2024-03-11T02:26:18.671407"))