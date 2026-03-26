import pandas as pd
from typing import Optional, Dict, Any
import os


def load_financial_transactions(
    file_path: str, **kwargs: Any
) -> Optional[pd.DataFrame]:
    """
    Функция для загрузки транзакций из CSV/XLSX.

    Args:
        file_path: путь к файлу с транзакциями
        **kwargs: дополнительные параметры для pd.read_csv()/pd.read_excel()

    Returns:
        DataFrame с данными или None при ошибке
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл не найден: {file_path}")

        if file_path.lower().endswith(".csv"):
            default_csv_params: Dict[str, Any] = {
                "sep": ",",
                "encoding": "utf-8",
                "header": 0,
                "skip_blank_lines": True,
            }
            # Объединяем параметры, отдавая приоритет пользовательским
            csv_params = {**default_csv_params, **kwargs}
            result = pd.read_csv(file_path, **csv_params)
            # Явно проверяем и приводим тип
            if isinstance(result, pd.DataFrame):
                df = result
                print(f"CSV загружен: {len(df)} записей")
            else:
                raise TypeError(f"Ожидался DataFrame, получено: {type(result)}")

        elif file_path.lower().endswith((".xlsx", ".xls")):
            default_excel_params: Dict[str, Any] = {"sheet_name": 0}
            excel_params = {**default_excel_params, **kwargs}
            result = pd.read_excel(file_path, **excel_params)
            # Явно проверяем и приводим тип
            if isinstance(result, pd.DataFrame):
                df = result
                print(f"Excel загружен: {len(df)} записей")
            else:
                raise TypeError(f"Ожидался DataFrame, получено: {type(result)}")
        else:
            raise ValueError(
                "Формат файла не поддерживается. Используйте CSV или XLSX."
            )
        return df
    except Exception as e:
        print(f"Ошибка загрузки {file_path}: {e}")
        return None


# Загрузка файлов
csv_data = load_financial_transactions("transactions.csv")
xlsx_data = load_financial_transactions("transactions_excel.xlsx")

# Проверка результатов
if csv_data is not None:
    print("\nПервые строки CSV:")
    print(csv_data.head())

if xlsx_data is not None:
    print("\nПервые строки XLSX:")
    print(xlsx_data.head())
