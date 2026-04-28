"""Вспомогательные утилиты для работы с CSV файлами."""

import csv
from pathlib import Path
from typing import List, Dict, Any


def read_csv_files(file_paths: List[Path]) -> List[Dict[str, Any]]:
    """
    Чтение данных из нескольких CSV файлов.

    Args:
        file_paths: Список путей к CSV файлам

    Returns:
        Список словарей с данными из всех файлов

    Raises:
        FileNotFoundError: Если файл не найден
        csv.Error: Если файл имеет некорректный CSV формат
    """
    all_data = []

    for file_path in file_paths:
        with open(file_path, "r", encoding="utf-8-sig") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                all_data.append(dict(row))

    return all_data
