from src.processing import filter_by_state, sort_by_date


def sample_data():
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-01-01T10:00:00"},
        {"id": 2, "state": "PENDING", "date": "2023-01-02T11:00:00"},
        {"id": 3, "state": "EXECUTED", "date": "2023-01-03T12:00:00"},
        {"id": 4, "state": "FAILED", "date": "2023-01-04T13:00:00"},
    ]


class TestProcessingFunctions:

    # Тесты для filter_by_state
    def test_filter_by_state_default(self):
        """Тест filter_by_state с состоянием по умолчанию (EXECUTED)."""
        result = filter_by_state(TEST_DATA)
        assert len(result) == 2
        assert all(item["state"] == "EXECUTED" for item in result)

    # Тесты для sort_by_date
    def test_sort_by_date_descending(self):
        """Тест sort_by_date — сортировка по убыванию даты (по умолчанию)."""
        result = sort_by_date(TEST_DATA)
        dates = [item["date"] for item in result]
        expected_dates = [
            "2023-01-04T13:00:00",  # id: 4 (самая новая дата)
            "2023-01-03T12:00:00",  # id: 3
            "2023-01-02T11:00:00",  # id: 2
            "2023-01-01T10:00:00",  # id: 1 (самая старая дата)
        ]
        assert [item["id"] for item in result] == [4, 3, 2, 1]
        assert dates == expected_dates
