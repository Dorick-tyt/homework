from src.processing import filter_by_state, sort_by_date

TEST_DATA = [
    {"id": 1, "state": "EXECUTED", "date": "2023-01-01T10:00:00"},
    {"id": 2, "state": "PENDING", "date": "2023-01-02T11:00:00"},
    {"id": 3, "state": "EXECUTED", "date": "2023-01-03T12:00:00"},
    {"id": 4, "state": "FAILED", "date": "2023-01-04T13:00:00"},
]

# Тесты для filter_by_state
result = filter_by_state(TEST_DATA)
assert len(result) == 2
assert all(item["state"] == "EXECUTED" for item in result)

# Тесты для sort_by_date
result = sort_by_date(TEST_DATA)
dates = [item["date"] for item in result]
expected_dates = [
    "2023-01-04T09:00:00",  # id: 4
    "2023-01-03T10:00:00",  # id: 1
    "2023-01-02T12:00:00",  # id: 3
    "2023-01-01T11:00:00",  # id: 2
]
assert [item["id"] for item in result] == [4, 1, 3, 2]
assert dates == expected_dates
