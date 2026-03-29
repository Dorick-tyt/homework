import csv
from typing import Any, Dict, List, Optional

import pandas as pd


def load_csv_transactions(
    file_path: str, keyseparator: str = ";"
) -> Optional[List[Dict[str, Any]]]:
    """Загрузка транзакций из CSV‑файла."""
    try:
        transactions: List[Dict[str, Any]] = []
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=";")
            for row in reader:
                processed_row = {
                    k.replace(";", keyseparator): v for k, v in row.items()
                }
                transactions.append(processed_row)
        print(f"Загружено {len(transactions)} транзакций из CSV")
        return transactions
    except FileNotFoundError:
        print(f"Ошибка: Файл {file_path} не найден")
        return None
    except Exception as e:
        print(f"Ошибка при загрузке CSV: {e}")
        return None


def load_excel_transactions(
    file_path: str, key_separator: str = ";"
) -> Optional[List[Dict[str, Any]]]:
    """Загрузка транзакций из Excel‑файла"""
    try:
        df = pd.read_excel(file_path)
        transactions: List[Dict[str, Any]] = [
            {str(k).replace(";", key_separator): v for k, v in row.items()}
            for row in df.to_dict("records")
        ]
        print(f"Загружено {len(transactions)} транзакций из Excel")
        return transactions
    except FileNotFoundError:
        print(f"Ошибка: Файл {file_path} не найден")
        return None
    except Exception as e:
        print(f"Ошибка при загрузке Excel: {e}")
        return None
