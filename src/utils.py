import json
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


def load_transactions(file_path: str) -> List[Dict]:
    """
    Загружает транзакции из JSON-файла.

    Args:
        file_path (str): Путь к JSON-файлу.

    Returns:
        List[Dict]: Список словарей с транзакциями или пустой список в случае ошибки.
    """
    logger.info(f"Попытка загрузить транзакции из файла: {file_path}")

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                logger.info(f"Успешно загружено {len(data)} транзакций из {file_path}")
                return data
            else:
                logger.error(f"Данные в файле {file_path} не являются списком")
                return []
    except FileNotFoundError:
        logger.warning(f"Файл не найден: {file_path}")
        return []
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка декодирования JSON в файле {file_path}: {e}")
        return []
    except IOError as e:
        logger.error(f"Ошибка ввода‑вывода при чтении файла {file_path}: {e}")
        return []
