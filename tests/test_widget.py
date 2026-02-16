def run_simple_tests():
    print("=== Тестирование mask_account_card ===")

    # Тест 1: Visa карта
    test1 = mask_account_card("Visa Platinum 7000792289606361")
    print(f"Тест 1: {test1}")
    assert test1 == "Visa Platinum 7000 79** **** 6361", "Ошибка в тесте 1"

    # Тест 2: Счёт
    test2 = mask_account_card("Счёт 40817810099910004312")
    print(f"Тест 2: {test2}")
    assert test2 == "Счёт **4312", "Ошибка в тесте 2"
    # Тест 3: Некорректная длина карты
    test3 = mask_account_card("Visa 1234")
    print(f"Тест 3: {test3}")
    assert test3 is None, "Ошибка в тесте 3"

    print("\n=== Тестирование get_date ===")
    # Тест 4: Корректная дата
    test4 = get_date("2024-03-11T02:26:18.671407")
    print(f"Тест 4: {test4}")
    assert test4 == "11.03.2024", "Ошибка в тесте 4"
    print("Все тесты пройдены!")


# Запуск простых тестов
run_simple_tests()