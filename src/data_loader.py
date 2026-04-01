import json
import os
from typing import Any, Dict, List, Optional

import pandas as pd


def load_financial_transactions(
    file_path: str, **kwargs: Any
) -> Optional[List[Dict[str, Any]]]:
    """
    Загружает транзакции из CSV/XLSX/JSON в виде списка словарей.

    Args:
        file_path: путь к файлу с транзакциями
        **kwargs: дополнительные параметры для чтения файлов

    Returns:
        Список словарей с транзакциями или None при ошибке
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл не найден: {file_path}")

        # Загрузка JSON-файла
        if file_path.lower().endswith(".json"):
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    result = data
                else:
                    print("Предупреждение: JSON-файл должен содержать массив объектов")
                    result = []

        # Загрузка CSV-файла
        elif file_path.lower().endswith(".csv"):
            default_csv_params: Dict[str, Any] = {
                "sep": ",",
                "encoding": "utf-8",
                "header": 0,
                "skip_blank_lines": True,
            }
            csv_params = {**default_csv_params, **kwargs}
            df = pd.read_csv(file_path, **csv_params)
            result = [
                {str(k): v for k, v in row.items()} for row in df.to_dict("records")
            ]
            print(f"CSV загружен: {len(result)} записей")

        # Загрузка Excel-файла (XLS/XLSX)
        elif file_path.lower().endswith((".xlsx", ".xls")):
            default_excel_params: Dict[str, Any] = {"sheet_name": 0}
            excel_params = {**default_excel_params, **kwargs}
            df = pd.read_excel(file_path, **excel_params)
            result = [
                {str(k): v for k, v in row.items()} for row in df.to_dict("records")
            ]
            print(f"Excel загружен: {len(result)} записей")
        else:
            raise ValueError(
                "Формат файла не поддерживается. Используйте JSON, CSV или XLSX."
            )
    except Exception as e:
        print(f"Ошибка загрузки {file_path}: {e}")
        return None

    return result
