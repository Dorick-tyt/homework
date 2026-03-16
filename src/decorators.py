import functools
import logging


def log(filename=None):
    """Декоратор для логирования выполнения функций."""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Настройка логирования
            if filename:
                log_handler = logging.FileHandler(filename, mode="a")
            else:
                log_handler = logging.StreamHandler()

            log_formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s: %(message)s"
            )
            log_handler.setFormatter(log_formatter)
            logging.getLogger().addHandler(log_handler)
            logging.getLogger().setLevel(logging.INFO)

            # Логирование начала выполнения функции
            logging.info(f"Start: {func.__name__}")

            try:
                # Выполнение функции
                result = func(*args, **kwargs)
                logging.info(f"End: {func.__name__} - Result: {result}")
                return result
            except Exception as e:
                logging.error(f"End: {func.__name__}")
                logging.error(f"Error: {type(e).__name__}, {e}")
                logging.error(f"Args: {args}, {kwargs}")
                raise
            finally:
                # Закрытие логгера (если логировались в файл)
                if filename:
                    log_handler.close()
                    logging.getLogger().removeHandler(log_handler)

        return wrapper

    return decorator
