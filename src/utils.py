import json
import os

from .logger_config import setup_logger

logger = setup_logger(__name__, "logs/utils.log")


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

    except json.JSONDecodeError as e:
        logger.error(f"Ошибка парсинга JSON в файле {file_path}: {e}")
        return []
    except IOError as e:
        logger.error(f"Ошибка ввода‑вывода при чтении файла {file_path}: {e}")
        return []
    except Exception as e:
        logger.critical(
            f"Неожиданная ошибка при загрузке транзакций из {file_path}: {e}"
        )
        return []
