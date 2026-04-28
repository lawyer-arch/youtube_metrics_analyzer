"""Вспомогательные утилиты для работы с CSV файлами."""

import csv
from pathlib import Path
from typing import List, Dict, Any


"""Вспомогательные утилиты для работы с CSV файлами."""

import csv
from pathlib import Path
from typing import List, Dict, Any


def read_csv_files(file_paths: List[Path]) -> List[Dict[str, Any]]:
    """Чтение данных из нескольких CSV файлов."""
    all_data = []
    
    for file_path in file_paths:
        with open(file_path, "r", encoding="utf-8-sig") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                clean_row = {}
                for key, value in row.items():
                    clean_key = key.strip().lstrip('\ufeff')
                    clean_row[clean_key] = value
                all_data.append(clean_row)
    
    return all_data
