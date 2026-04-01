import logging
from unittest.mock import patch

import pytest

from src.decorators import log


class TestLogDecorator:
    """Тесты для декоратора логирования log."""

    def test_basic_function_logging(self):
        """Тест базового логирования функции."""

        @log()
        def test_func(x, y):
            return x + y

        with patch.object(
            logging.getLogger("decorator.test_func"), "info"
        ) as mock_info:
            result = test_func(5, 3)
            assert result == 8
            # Проверяем, что логирование вызывалось
            assert mock_info.call_count == 2
            # Проверяем сообщения
            first_call = mock_info.call_args_list[0][0][0]
            second_call = mock_info.call_args_list[1][0][0]
            assert "Start: test_func" in first_call
            assert "End: test_func - Result: 8" in second_call

    def test_file_logging(self, tmp_path):
        """Тест логирования в файл."""
        log_file = tmp_path / "test_log.txt"

        @log(filename=str(log_file))
        def simple_func():
            return "OK"

        result = simple_func()
        assert result == "OK"
        # Проверяем, что файл создан и содержит логи
        assert log_file.exists()
        content = log_file.read_text(encoding="utf-8")
        assert "Start: simple_func" in content
        assert "End: simple_func - Result: OK" in content

    def test_exception_logging(self):
        """Тест логирования исключений."""

        @log()
        def error_func():
            raise ValueError("Test error")

        with pytest.raises(ValueError, match="Test error"):
            error_func()

        # Проверяем логирование ошибки
        logger = logging.getLogger("decorator.error_func")
        with patch.object(logger, "error") as mock_error:
            try:
                error_func()
            except ValueError:
                pass
            assert mock_error.call_count >= 2  # минимум 2 сообщения об ошибке
            error_calls = [call[0][0] for call in mock_error.call_args_list]
            assert any("Error: ValueError, Test error" in msg for msg in error_calls)

    def test_keyboard_interrupt_logging(self):
        """Тест логирования KeyboardInterrupt."""

        @log()
        def interrupt_func():
            raise KeyboardInterrupt()

        with pytest.raises(KeyboardInterrupt):
            interrupt_func()

        logger = logging.getLogger("decorator.interrupt_func")
        with patch.object(logger, "error") as mock_error:
            try:
                interrupt_func()
            except KeyboardInterrupt:
                pass
            error_messages = [call[0][0] for call in mock_error.call_args_list]
            assert any("Interrupted by user" in msg for msg in error_messages)

    def test_system_exit_logging(self):
        """Тест логирования SystemExit."""

        @log()
        def exit_func():
            raise SystemExit()

        with pytest.raises(SystemExit):
            exit_func()

        logger = logging.getLogger("decorator.exit_func")
        with patch.object(logger, "error") as mock_error:
            try:
                exit_func()
            except SystemExit:
                pass
            error_messages = [call[0][0] for call in mock_error.call_args_list]
            assert any("System exit" in msg for msg in error_messages)

    def test_function_with_args_kwargs(self):
        """Тест функции с аргументами и kwargs."""

        @log()
        def complex_func(a, b, c=None, debug=False):
            if debug:
                return f"Debug: {a}, {b}, {c}"
            return a * b + (c or 0)

        with patch.object(
            logging.getLogger("decorator.complex_func"), "info"
        ) as mock_info:
            # Тест с позиционными аргументами
            result1 = complex_func(2, 3, c=1)
            assert result1 == 7

            # Тест с kwargs
            result2 = complex_func(1, 2, debug=True)
            assert "Debug: 1, 2, None" in result2

            # Проверяем логи
            info_messages = [call[0][0] for call in mock_info.call_args_list]
            assert any("Start: complex_func" in msg for msg in info_messages)
            assert any("End: complex_func - Result: 7" in msg for msg in info_messages)

    def test_return_types(self):
        """Тест разных типов возвращаемых значений."""
        test_cases = [
            (lambda: 42, "int"),
            (lambda: "string", "str"),
            (lambda: [1, 2, 3], "list"),
            (lambda: {"key": "value"}, "dict"),
            (lambda: None, "None"),
        ]

        for func, expected_type in test_cases:
            decorated = log()(func)
            with patch.object(
                logging.getLogger(f"decorator.{func.__name__}"), "info"
            ) as mock_info:
                result = decorated()
                info_messages = [call[0][0] for call in mock_info.call_args_list]
                assert any(f"End: {func.__name__}" in msg for msg in info_messages)
                if expected_type != "None":
                    assert f"Result: {result}" in " ".join(info_messages)

    def test_multiple_decorator_calls(self):
        """Тест многократного вызова декорированной функции."""
        call_count = 0  # Внешняя переменная

        @log()
        def counter_func():
            nonlocal call_count
            call_count += 1
            return call_count

        results = []
        with patch.object(
            logging.getLogger("decorator.counter_func"), "info"
        ) as mock_info:
            for i in range(3):
                result = counter_func()
                results.append(result)

        assert results == [1, 2, 3]
        assert mock_info.call_count == 6

    def test_handler_cleanup(self):
        """Тест очистки обработчиков логгера."""

        @log()
        def cleanup_test():
            return "test"

        logger = logging.getLogger("decorator.cleanup_test")
        initial_handlers = len(logger.handlers)

        cleanup_test()
        final_handlers = len(logger.handlers)
        # После выполнения обработчики должны быть удалены
        assert final_handlers == initial_handlers

    def test_no_filename_uses_stdout(self):
        """Тест использования stdout при отсутствии filename."""

        @log()  # без filename
        def stdout_test():
            return "stdout"

        with patch.object(logging.StreamHandler, "emit") as mock_emit:
            stdout_test()
            # Проверяем, что использовался StreamHandler
            assert mock_emit.call_count > 0

    @pytest.mark.parametrize(
        "input_value,expected",
        [
            (5, "int"),
            ("hello", "str"),
            ([1, 2], "list"),
            ({"a": 1}, "dict"),
        ],
    )
    def test_parametrized_logging(self, input_value, expected):
        """Параметризованные тесты для разных входных данных."""

        @log()
        def process_data(data):
            return f"Processed: {data}"

        with patch.object(
            logging.getLogger("decorator.process_data"), "info"
        ) as mock_info:
            result = process_data(input_value)
            assert f"Processed: {input_value}" == result

            # Извлекаем все сообщения из вызовов info()
            info_messages = [call[0][0] for call in mock_info.call_args_list]

            # Проверяем наличие стартового сообщения (без f-строки)
            assert any("Start: process_data" in msg for msg in info_messages)

            # Проверяем сообщение с результатом (f-строка с заполнителем)
            expected_result_msg = f"Result: Processed: {input_value}"
            assert any(expected_result_msg in msg for msg in info_messages)
