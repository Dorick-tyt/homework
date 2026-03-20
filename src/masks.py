import logging  # импортируем logging

# Получаем логер для модуля masks
logger = logging.getLogger(__name__)

def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер банковской карты.
    Формат вывода: XXXX XX** **** XXXX (видны первые 6 и последние 4 цифры, остальное — звёздочки;
    разбивка по 4 цифры через пробел).
    """
    logger.info(f"Начало маскирования номера карты: {card_number}")

    # Удаляем пробелы и дефисы
    cleaned = card_number.replace(" ", "").replace("-", "")

    # Проверяем, что строка содержит только цифры
    if not cleaned.isdigit():
        error_msg = "Номер карты должен содержать только цифры"
        logger.error(error_msg)
        raise ValueError(error_msg)

    # Проверяем длину — должна быть 16 цифр
    if len(cleaned) != 16:
        error_msg = "Номер карты должен содержать 16 цифр"
        logger.error(error_msg)
        raise ValueError(error_msg)

    # Формируем маску
    masked = cleaned[:4] + " " + cleaned[4:6] + "** **** " + cleaned[-4:]
    logger.info(f"Номер карты успешно замаскирован: {masked}")
    return masked


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер банковского счёта.
    Формат вывода: **XXXX (видны только последние 4 цифры, перед ними — две звёздочки).
    """
    logger.info(f"Начало маскирования номера счёта: {account_number}")

    # Удаляем пробелы
    cleaned = account_number.replace(" ", "")

    # Проверяем, что строка содержит только цифры
    if not cleaned.isdigit():
        error_msg = "Номер счёта должен содержать только цифры"
        logger.error(error_msg)
        raise ValueError(error_msg)

    # Проверяем минимальную длину
    if len(cleaned) < 4:
        error_msg = "Номер счёта слишком короткий"
        logger.error(error_msg)
        raise ValueError(error_msg)

    # Берём последние 4 цифры
    last_num = cleaned[-4:]
    # Формируем маску: две звёздочки + последние 4 цифры
    masked = "**" + last_num
    logger.info(f"Номер счёта успешно замаскирован: {masked}")
    return masked
