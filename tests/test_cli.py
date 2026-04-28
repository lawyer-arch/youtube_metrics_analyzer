"""Тесты для CLI модуля."""

import pytest
from pathlib import Path
import tempfile
import csv
from unittest.mock import patch

from src.cli import validate_files, parse_arguments


class TestCLI:
    """Тесты для CLI функций."""

    @pytest.fixture
    def temp_csv_file(self) -> Path:
        """Фикстура временного CSV файла."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False, encoding="utf-8"
        ) as tmp:
            writer = csv.writer(tmp)
            writer.writerow(["title", "ctr", "retention_rate", "views"])
            writer.writerow(["Test Video", "20.5", "35", "1000"])
            return Path(tmp.name)

    @pytest.fixture
    def temp_empty_file(self) -> Path:
        """Фикстура пустого временного файла."""
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
            tmp.write(b"")
            return Path(tmp.name)

    def test_validate_files_existing(self, temp_csv_file: Path):
        """Тест валидации существующего файла."""
        result = validate_files([str(temp_csv_file)])
        assert len(result) == 1
        assert result[0] == temp_csv_file

    def test_validate_multiple_files(self, temp_csv_file: Path):
        """Тест валидации нескольких файлов."""
        result = validate_files([str(temp_csv_file), str(temp_csv_file)])
        assert len(result) == 2
        assert result[0] == temp_csv_file
        assert result[1] == temp_csv_file

    def test_validate_files_not_existing(self, capsys):
        """Тест валидации несуществующего файла."""
        with pytest.raises(SystemExit):
            validate_files(["nonexistent_file.csv"])

        captured = capsys.readouterr()
        assert "Файл не найден" in captured.err

    def test_validate_not_a_file(self, temp_empty_file: Path, capsys):
        """Тест валидации пути, не являющегося файлом."""
        with pytest.raises(SystemExit):
            validate_files([str(temp_empty_file)])

        captured = capsys.readouterr()
        assert "не является файлом" in captured.err

    @patch("sys.argv", ["main.py", "--files", "data.csv", "--report", "clickbait"])
    def test_parse_arguments_valid(self):
        """Тест парсинга валидных аргументов."""
        args = parse_arguments()
        assert args.files == ["data.csv"]
        assert args.report == "clickbait"

    @patch("sys.argv", ["main.py", "--files", "file1.csv", "file2.csv", "--report", "clickbait"])
    def test_parse_arguments_multiple_files(self):
        """Тест парсинга нескольких файлов."""
        args = parse_arguments()
        assert args.files == ["file1.csv", "file2.csv"]
        assert args.report == "clickbait"

    def test_parse_arguments_missing_files(self):
        """Тест отсутствия обязательного параметра --files."""
        with patch("sys.argv", ["main.py", "--report", "clickbait"]):
            with pytest.raises(SystemExit):
                parse_arguments()

    def test_parse_arguments_missing_report(self):
        """Тест отсутствия обязательного параметра --report."""
        with patch("sys.argv", ["main.py", "--files", "data.csv"]):
            with pytest.raises(SystemExit):
                parse_arguments()

    def test_parse_arguments_invalid_report(self):
        """Тест с недопустимым значением --report."""
        with patch("sys.argv", ["main.py", "--files", "data.csv", "--report", "invalid"]):
            with pytest.raises(SystemExit):
                parse_arguments()
