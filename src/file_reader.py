import csv
import os
from typing import Any, Dict, List, Optional

import pandas as pd


def load_csv_transactions(
    file_path: str, **kwargs: Any
) -> Optional[List[Dict[str, Any]]]:
    """
    Функция для загрузки финансовых операций из CSV‑файла.

    Args:
        file_path: путь к CSV‑файлу с транзакциями
        **kwargs: дополнительные параметры для csv.DictReader или pd.read_csv()

    Returns:
        Список словарей с транзакциями или None при ошибке
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл не найден: {file_path}")

        # Используем csv.reader для большей гибкости
        with open(file_path, "r", encoding=kwargs.get("encoding", "utf-8")) as f:
            csv_params = {
                "delimiter": kwargs.get("delimiter", ","),
                "quotechar": kwargs.get("quotechar", '"'),
            }
            reader = csv.DictReader(f, **csv_params)
            result: List[Dict[str, Any]] = []
            for row in reader:
                # Приводим ключи к строкам (на всякий случай)
                cleaned_row = {str(k): v for k, v in row.items()}
                result.append(cleaned_row)
        print(f"CSV загружен: {len(result)} записей")
        return result

    except Exception as e:
        print(f"Ошибка загрузки CSV {file_path}: {e}")
        return None


def load_excel_transactions(
    file_path: str, **kwargs: Any
) -> Optional[List[Dict[str, Any]]]:
    """
    Функция для загрузки финансовых операций из Excel‑файла (XLSX/XLS).

    Args:
        file_path: путь к Excel‑файлу с транзакциями
        **kwargs: дополнительные параметры для pd.read_excel()

    Returns:
        Список словарей с транзакциями или None при ошибке
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл не найден: {file_path}")

        default_excel_params: Dict[str, Any] = {"sheet_name": 0}
        excel_params = {**default_excel_params, **kwargs}
        df = pd.read_excel(file_path, **excel_params)
        result: List[Dict[str, Any]] = [
            {str(k): v for k, v in row.items()} for row in df.to_dict("records")
        ]
        print(f"Excel загружен: {len(result)} записей")
        return result

    except Exception as e:
        print(f"Ошибка загрузки Excel {file_path}: {e}")
        return None
