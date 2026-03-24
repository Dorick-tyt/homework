import json
import logging
import os

from .logger_config import setup_module_logger

logger = setup_module_logger("utils", "logs/utils.log", level=logging.DEBUG)

try:
    logger.info("Логгер модуля utils успешно инициализирован")
except Exception as setup_exc:
    print(f"КРИТИЧЕСКАЯ ОШИБКА: Не удалось настроить логгер utils: {setup_exc}")
    raise


def load_transactions(file_path: str) -> list:
    """Загружает транзакции из JSON‑файла."""
    logger.debug(f"Попытка загрузить транзакции из файла: {file_path}")

    try:
        # Проверяем существование файла
        if not os.path.exists(file_path):
            logger.error(f"Файл не найден: {file_path}")
            return []

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Проверяем, что данные — список
        if not isinstance(data, list):
            logger.error(f"Данные в файле {file_path} не являются списком")
            return []

        logger.info(f"Успешно загружено {len(data)} транзакций из {file_path}")
        return data

    except json.JSONDecodeError as json_exc:
        logger.error(f"Ошибка парсинга JSON в файле {file_path}: {json_exc}")
        return []
    except IOError as io_exc:
        logger.error(f"Ошибка ввода‑вывода при чтении файла {file_path}: {io_exc}")
        return []
    except Exception as general_exc:
        logger.critical(
            f"Неожиданная ошибка при загрузке транзакций из {file_path}: {general_exc}"
        )
        return []
