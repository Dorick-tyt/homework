import functools
import logging
import sys
from typing import Any, Callable, Optional, TypeVar

# Для старых версий Python используем TypeVar для аргументов
T = TypeVar("T")
R = TypeVar("R")


def log(
    filename: Optional[str] = None,
) -> Callable[[Callable[..., R]], Callable[..., R]]:
    """Декоратор для логирования выполнения функций."""

    def decorator(func: Callable[..., R]) -> Callable[..., R]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> R:
            logger = logging.getLogger(f"decorator.{func.__name__}")

            # Настройка логирования
            if filename:
                log_handler: logging.Handler = logging.FileHandler(
                    filename, mode="a", encoding="utf-8"
                )
            else:
                log_handler = logging.StreamHandler(sys.stdout)

            log_formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s: %(message)s"
            )
            log_handler.setFormatter(log_formatter)
            logger.addHandler(log_handler)
            logger.setLevel(logging.INFO)

            # Логирование начала выполнения функции
            logger.info(f"Start: {func.__name__}")

            try:
                # Выполнение функции
                result: R = func(*args, **kwargs)
                logger.info(f"End: {func.__name__} - Result: {result}")
                return result

            except KeyboardInterrupt:
                logger.error(f"End: {func.__name__} - Interrupted by user")
                raise

            except SystemExit:
                logger.error(f"End: {func.__name__} - System exit")
                raise

            except Exception as e:
                logger.error(f"End: {func.__name__}")
                logger.error(f"Error: {type(e).__name__}, {e}")
                logger.error(f"Args: {args}, {kwargs}")
                # Пробрасываем исключение дальше
                raise

            finally:
                # Гарантированная очистка обработчика
                try:
                    log_handler.close()
                    logger.removeHandler(log_handler)
                except Exception:
                    pass  # Игнорируем ошибки при очистке

        return wrapper

    return decorator
