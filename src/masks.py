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


def mask_card_number(card_number: str) -> str:
    # Очищаем от нечисловых символов
    cleaned = re.sub(r"\D", "", card_number)
    if logger is not None:
        logger.debug(f"Попытка замаскировать номер карты: {card_number}")

    if len(cleaned) != 16:
        if logger is not None:
            logger.error(f"Некорректная длина номера карты: {len(cleaned)} цифр")
        return "Номер карты должен содержать 16 цифр"

    # Маскируем номер
    masked = f"{cleaned[:6]}****{cleaned[-4:]}"
    if logger is not None:
        logger.info(f"Номер карты успешно замаскирован: {masked}")
    return masked


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
