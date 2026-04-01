import logging
import os
import re
from typing import Optional


def setup_logger() -> Optional[logging.Logger]:
    log_file = "logs/masks.log"
    log_dir = os.path.dirname(log_file)

    try:
        os.makedirs(log_dir, exist_ok=True)
        logging.info(f"Создана директория для логов: {log_dir}")
    except Exception as exc:
        print(f"Ошибка создания директории: {exc}")
        return None

    local_logger = logging.getLogger("masks")
    local_logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    local_logger.addHandler(file_handler)
    return local_logger


# Получаем логгер при первом вызове
logger = setup_logger()


def mask_card_number(card_info: str) -> str:
    """
    Маскирует номер карты или счета.
    Для карт: Visa 1234567890123456 -> Visa 1234 56** **** 3456
    Для счетов: Счет 12345678901234567890 -> Счет **7890
    """
    if not card_info or not isinstance(card_info, str):
        return ""

    # Разделяем тип и номер
    parts = card_info.split()
    if len(parts) < 2:
        return card_info

    card_type = " ".join(parts[:-1])  # Тип карты/счета
    number = parts[-1]  # Номер

    # Проверяем, что номер состоит из цифр
    if not number.isdigit():
        return card_info

    # Если это счет (обычно 20 цифр)
    if len(number) == 20:
        masked = f"**{number[-4:]}"
        return f"{card_type} {masked}"

    # Если это карта (16 цифр)
    elif len(number) == 16:
        masked = f"{number[:4]} {number[4:6]}** **** {number[-4:]}"
        return f"{card_type} {masked}"

    # Для других форматов (например, Maestro 1596837868705199 - 16 цифр)
    elif len(number) >= 16:
        # Берем последние 4 цифры
        masked = f"**{number[-4:]}"
        return f"{card_type} {masked}"

    return card_info


def mask_account_number(account_number: str) -> str:
    # Очищаем от нечисловых символов
    cleaned = re.sub(r"\D", "", account_number)
    if logger is not None:
        logger.debug(f"Попытка замаскировать номер счёта: {account_number}")

    if len(cleaned) < 4:
        if logger is not None:
            logger.error(f"Слишком короткий номер счёта: {len(cleaned)} цифр")
        return "Номер счёта должен содержать минимум 4 цифры"

    # Маскируем номер — показываем только последние 4 цифры
    masked = "**" + cleaned[-4:]
    if logger is not None:
        logger.info(f"Номер счёта успешно замаскирован: {masked}")
    return masked
