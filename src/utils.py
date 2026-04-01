import json
import logging
import os
from typing import Any, Dict, Optional


def setup_logger() -> Optional[logging.Logger]:
    log_file = "logs/utils.log"
    log_dir = os.path.dirname(log_file)

    try:
        os.makedirs(log_dir, exist_ok=True)
        logging.info(f"Создана директория для логов: {log_dir}")
    except Exception as exc:
        print(f"Ошибка создания директории: {exc}")
        return None

    local_logger = logging.getLogger("utils")
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


def load_transactions(file_path: str) -> list[Dict[str, Any]]:
    """Загружает транзакции из JSON‑файла."""
    if logger is None:
        # Если логгер не инициализирован, используем print
        print(f"Попытка загрузить транзакции из файла: {file_path}")
    else:
        logger.debug(f"Попытка загрузить транзакции из файла: {file_path}")

    try:
        # Проверяем существование файла
        if not os.path.exists(file_path):
            if logger:
                logger.error(f"Файл не найден: {file_path}")
            else:
                print(f"Файл не найден: {file_path}")
            return []

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Проверяем, что данные — список
        if not isinstance(data, list):
            if logger:
                logger.error(f"Данные в файле {file_path} не являются списком")
            else:
                print(f"Данные в файле {file_path} не являются списком")
            return []

        if logger:
            logger.info(f"Успешно загружено {len(data)} транзакций из {file_path}")
        else:
            print(f"Успешно загружено {len(data)} транзакций из {file_path}")
        return data

    except json.JSONDecodeError as json_exc:
        if logger:
            logger.error(f"Ошибка парсинга JSON в файле {file_path}: {json_exc}")
        else:
            print(f"Ошибка парсинга JSON в файле {file_path}: {json_exc}")
        return []
    except IOError as io_exc:
        if logger:
            logger.error(f"Ошибка ввода‑вывода при чтении файла {file_path}: {io_exc}")
        else:
            print(f"Ошибка ввода‑вывода при чтении файла {file_path}: {io_exc}")
        return []
    except Exception as general_exc:
        if logger:
            logger.critical(
                f"Неожиданная ошибка при загрузке транзакций из {file_path}: {general_exc}"
            )
        else:
            print(
                f"Неожиданная ошибка при загрузке транзакций из {file_path}: {general_exc}"
            )
        return []
