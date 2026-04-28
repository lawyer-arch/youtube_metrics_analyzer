"""CLI интерфейс приложения."""

import argparse
import sys
from pathlib import Path
from typing import List, Dict, Any

from tabulate import tabulate

from src.reporters import get_reporter
from src.utils import read_csv_files


def parse_arguments() -> argparse.Namespace:
    """Парсинг аргументов командной строки."""
    parser = argparse.ArgumentParser(
        description="Анализ метрик YouTube видео и формирование отчётов",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры:
  %(prog)s --files stats1.csv --report clickbait
  %(prog)s --files stats1.csv stats2.csv --report clickbait
        """,
    )
    parser.add_argument(
        "--files", nargs="+", required=True, help="Пути к CSV файлам с метриками"
    )
    parser.add_argument(
        "--report",
        required=True,
        choices=["clickbait"],
        help="Тип отчёта для формирования",
    )
    return parser.parse_args()


def validate_files(file_paths: List[str]) -> List[Path]:
    """Проверка существования файлов."""
    valid_paths = []
    for file_path in file_paths:
        path = Path(file_path)
        if not path.exists():
            print(f"Ошибка: Файл не найден: {file_path}", file=sys.stderr)
            sys.exit(1)
        if not path.is_file():
            print(f"Ошибка: Путь не является файлом: {file_path}", file=sys.stderr)
            sys.exit(1)
        # Также проверяем, что файл имеет расширение .csv
        if path.suffix.lower() != '.csv':
            print(f"Ошибка: Файл не является CSV: {file_path}", file=sys.stderr)
            sys.exit(1)
        valid_paths.append(path)
    return valid_paths


def print_report(report_data: List[Dict[str, Any]], headers: List[str]) -> None:
    """Вывод отчёта в виде таблицы."""
    if not report_data:
        print("Отчёт не содержит данных, соответствующих критериям.")
        return

    table_data = [[item[header] for header in headers] for item in report_data]

    print(tabulate(table_data, headers=headers, tablefmt="grid"))


def main() -> None:
    """Основная функция приложения."""
    args = parse_arguments()

    # Валидация файлов
    file_paths = validate_files(args.files)

    # Чтение данных
    try:
        all_data = read_csv_files(file_paths)
    except Exception as e:
        print(f"Ошибка при чтении файлов: {e}", file=sys.stderr)
        sys.exit(1)

    # Получение репортера и формирование отчёта
    try:
        reporter_class = get_reporter(args.report)
        reporter = reporter_class()
        report_data = reporter.generate(all_data)
        headers = reporter.get_headers()
        print_report(report_data, headers)
    except ValueError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка при формировании отчёта: {e}", file=sys.stderr)
        sys.exit(1)
