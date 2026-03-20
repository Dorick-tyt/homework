import logging
from pathlib import Path

def setup_logging():
    """
    Настраивает логирование для всего проекта.
    Создаёт папку logs, если её нет, и настраивает логеры для модулей.
    """
    # Создаём папку logs в корне проекта
    logs_dir = Path(__file__).parent.parent / "logs"
    logs_dir.mkdir(exist_ok=True)

    # Формат логов: время, модуль, уровень, сообщение
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(log_format)

    # Обработчик для записи в файл (перезаписывает при каждом запуске)
    file_handler = logging.FileHandler(
        logs_dir / "app.log",
        mode='w',  # перезапись при каждом запуске
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)

    # Настраиваем корневого логера
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)

    # Отключаем дублирование в консоль (если нужно)
    root_logger.propagate = False

    return root_logger

# Инициализируем логирование при импорте модуля
logger = setup_logging()