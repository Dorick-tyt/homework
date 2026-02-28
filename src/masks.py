def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер банковской карты.
    Формат вывода: XXXX XX** **** XXXX (видны первые 6 и последние 4 цифры, остальное — звёздочки;
    разбивка по 4 цифры через пробел).
    """
    # Удаляем пробелы и дефисы
    cleaned = card_number.replace(" ", "").replace("-", "")

    # Проверяем, что строка содержит только цифры
    if not cleaned.isdigit():
        return str(ValueError("Номер карты должен содержать только цифры"))

    # Проверяем длину — должна быть 16 цифрФормируем маску
    if len(cleaned) != 16:
        return str(ValueError("Номер карты должен содержать 16 цифр"))

    # Формируем маску
    masked = cleaned[:4] + " " + cleaned[4:6] + "** **** " + cleaned[-4:]
    return masked


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер банковского счёта.
    Формат вывода: **XXXX (видны только последние 4 цифры, перед ними — две звёздочки).
    """
    # Удаляем пробелы
    cleaned = account_number.replace(" ", "")

    # Проверяем, что строка содержит только цифры
    if not cleaned.isdigit():
        return str(ValueError("Номер счёта должен содержать только цифры"))

    # Проверяем минимальную длину
    if len(cleaned) < 4:
        return str(ValueError("Номер счёта слишком короткий"))

    # Берём последние 4 цифры
    last_num = cleaned[-4:]
    # Формируем маску: две звёздочки + последние 4 цифры
    masked = "**" + last_num

    return masked
