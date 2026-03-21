import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(name: str, log_file: str) -> logging.Logger:
    """
    Создаёт и настраивает логер с file_handler и форматированием.

    Args:
        name: имя логера (обычно __name__)
        log_file: путь к файлу логов

    Returns:
        Настроенный объект Logger
    """
    # Создаём логер
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Уровень не ниже DEBUG

    # Удаляем существующие обработчики, чтобы избежать дублирования
    logger.handlers.clear()

    # Создаём директорию для логов, если её нет
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    # Настраиваем file_handler с ротацией
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10 МБ
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)

    # Настраиваем formatter
    file_formatter = logging.Formatter(
        '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)

    # Добавляем обработчик к логеру
    logger.addHandler(file_handler)

    return logger
