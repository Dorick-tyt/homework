from src.masks import get_mask_card_number, get_mask_account


def test_get_mask_card_number_non_digit_characters():
    """Тест с нечисловыми символами в номере карты."""
    result = get_mask_card_number("1234abcd5678efgh")
    assert "Номер карты должен содержать только цифры" in str(result)


def test_get_mask_card_number_empty_string():
    """Тест с пустой строкой."""
    result = get_mask_card_number("")
    assert "Номер карты должен содержать только цифры" in str(result)


def test_get_mask_card_number_invalid_length():
    """Тест с номером карты неправильной длины (не 16 цифр)."""
    result = get_mask_card_number("12345678")
    assert "Номер карты должен содержать 16 цифр" in str(result)


def test_get_mask_card_number_single_digit():
    """Тест с одноцифровым номером счёта."""
    result = get_mask_card_number("5")
    assert "Номер карты должен содержать 16 цифр" in str(result)


# Тесты для get_mask_account
def test_get_mask_account_non_digit_characters():
    """Тест с нечисловыми символами в номере счёта."""
    result = get_mask_account("1234abcd")
    assert "Номер счёта должен содержать только цифры" in str(result)


def test_get_mask_account_too_short():
    """Тест с слишком коротким номером счёта (меньше 4 цифр)."""
    result = get_mask_account("123")
    assert "Номер счёта слишком короткий" in str(result)
