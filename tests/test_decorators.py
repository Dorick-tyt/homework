import pytest
from src.decorators import log


def test_log_console(capsys):
    @log()  # Логирование в консоль
    def test_function():
        return "Success"

    test_function()
    captured = capsys.readouterr()

    assert "Start: test_function" in captured.err
    assert "End: test_function - Result: Success" in captured.err


def test_log_file(tmp_path):
    filename = tmp_path / "test_log.txt"

    @log(filename=filename)  # Логирование в файл
    def test_function():
        return "Success"

    test_function()

    with open(filename, "r") as f:
        content = f.read()
        assert "Start: test_function" in content
        assert "End: test_function - Result: Success" in content
        assert "INFO:" in content


def test_log_exception(capsys):
    @log()
    def test_function():
        raise ValueError("Test error")

    with pytest.raises(ValueError, match="Test error"):
        test_function()

    captured = capsys.readouterr()
    assert "Start: test_function" in captured.err
    assert "End: test_function" in captured.err
    assert "Error: ValueError, Test error" in captured.err
    assert "Args: (), {}" in captured.err  # пустые аргументы и kwargs
