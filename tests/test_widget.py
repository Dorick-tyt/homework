from src.masks import get_mask_account, get_mask_card_number
from src.widget import get_date


class TestWidgetFunctions:

    def test_get_mask_card_number_valid(self):
        """Тест маскировки корректного номера карты (только цифры)."""
        result = get_mask_card_number("7000792289606361")
        assert result == "7000 79** **** 6361"

    def test_get_mask_card_number_non_digits(self):
        """Тест с нечисловыми символами в номере карты."""
        result = get_mask_card_number("Visa Platinum 7000792289606361")
        assert "Номер карты должен содержать только цифры" in str(result)

    def test_get_mask_account_valid(self):
        """Тест маскировки корректного номера счёта."""
        result = get_mask_account("40817810099910004312")
        assert result == "**4312"

    def test_get_mask_account_non_digits(self):
        """Тест с нечисловыми символами в номере счёта."""
        result = get_mask_account("Счёт 40817810099910004312")
        assert "Номер счёта должен содержать только цифры" in str(result)

    def test_get_mask_account_too_short(self):
        """Тест с слишком коротким номером счёта."""
        result = get_mask_account("123")
        assert "Номер счёта слишком короткий" in str(result)

    def test_get_date_valid_input(self):
        """Тест преобразования даты."""
        result = get_date("2024-03-11T02:26:18.671407")
        assert result == "11.03.2024"
