import logging
import os
from logging.handlers import RotatingFileHandler


def setup_module_logger(
    module_name: str, log_file: str, level: int = logging.DEBUG
) -> logging.Logger:
    """
    Создаёт и настраивает отдельный логгер для конкретного модуля.
    """
    # Создаём директорию для логов с обработкой ошибок
    log_dir = os.path.dirname(log_file)
    try:
        os.makedirs(log_dir, exist_ok=True)
        logging.info(f"Директория {log_dir} создана или уже существует")
    except PermissionError:
        raise PermissionError(f"Нет прав на создание директории {log_dir}")
    except Exception as exc:
        raise RuntimeError(f"Ошибка создания директории {log_dir}: {exc}")

    # Получаем логер (или создаём новый)
    logger = logging.getLogger(module_name)

    # Очищаем старые обработчики, чтобы избежать дублирования
    logger.handlers.clear()

    logger.setLevel(level)

    # Форматировщик
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Обработчик для файла
    try:
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10 МБ
            backupCount=5,
            encoding="utf-8",  # Явная кодировка
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except PermissionError:
        raise PermissionError(f"Нет прав на запись в файл {log_file}")
    except Exception as exc:
        raise RuntimeError(f"Ошибка создания обработчика для {log_file}: {exc}")

    return logger
