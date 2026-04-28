"""Тесты для утилит."""

import pytest
import tempfile
import csv
from pathlib import Path

from src.utils import read_csv_files


class TestUtils:
    """Тесты для утилит."""

    @pytest.fixture
    def valid_csv_file(self) -> Path:
        """Фикстура валидного CSV файла."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False, encoding="utf-8"
        ) as tmp:
            writer = csv.writer(tmp)
            writer.writerow(["title", "ctr", "retention_rate", "views"])
            writer.writerow(["Video 1", "18.2", "35", "45200"])
            writer.writerow(["Video 2", "22.5", "28", "128700"])
            return Path(tmp.name)

    @pytest.fixture
    def second_csv_file(self) -> Path:
        """Фикстура второго CSV файла."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False, encoding="utf-8"
        ) as tmp:
            writer = csv.writer(tmp)
            writer.writerow(["title", "ctr", "retention_rate", "views"])
            writer.writerow(["Video 3", "25.0", "22", "254000"])
            writer.writerow(["Video 4", "9.5", "82", "31500"])
            return Path(tmp.name)

    def test_read_single_csv_file(self, valid_csv_file: Path):
        """Тест чтения одного CSV файла."""
        result = read_csv_files([valid_csv_file])
        assert len(result) == 2
        assert result[0]["title"] == "Video 1"
        assert result[0]["ctr"] == "18.2"
        assert result[0]["retention_rate"] == "35"
        assert result[1]["title"] == "Video 2"

    def test_read_multiple_csv_files(self, valid_csv_file: Path, second_csv_file: Path):
        """Тест чтения нескольких CSV файлов."""
        result = read_csv_files([valid_csv_file, second_csv_file])
        assert len(result) == 4
        titles = [row["title"] for row in result]
        assert "Video 1" in titles
        assert "Video 2" in titles
        assert "Video 3" in titles
        assert "Video 4" in titles

    def test_read_empty_csv_file(self):
        """Тест чтения CSV файла только с заголовками."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False, encoding="utf-8"
        ) as tmp:
            writer = csv.writer(tmp)
            writer.writerow(["title", "ctr", "retention_rate"])

        result = read_csv_files([Path(tmp.name)])
        assert result == []

    def test_read_csv_with_different_columns(self):
        """Тест чтения CSV с дополнительными колонками."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False, encoding="utf-8"
        ) as tmp:
            writer = csv.writer(tmp)
            writer.writerow(["title", "ctr", "retention_rate", "extra", "another"])
            writer.writerow(["Video 1", "15.5", "45", "extra_data", "more_data"])
            writer.writerow(["Video 2", "20.0", "30", "test", "test2"])

        result = read_csv_files([Path(tmp.name)])
        assert len(result) == 2
        assert "extra" in result[0]
        assert result[0]["extra"] == "extra_data"

    def test_read_csv_with_utf8_bom(self):
        """Тест чтения CSV с BOM (Byte Order Mark)."""
        content = "\ufefftitle,ctr,retention_rate\nVideo,18.2,35"
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False, encoding="utf-8-sig"
        ) as tmp:
            tmp.write(content)

        result = read_csv_files([Path(tmp.name)])
        assert len(result) == 1
        assert result[0]["title"] == "Video"
        assert result[0]["ctr"] == "18.2"

    def test_file_not_found(self):
        """Тест обработки несуществующего файла."""
        with pytest.raises(FileNotFoundError):
            read_csv_files([Path("nonexistent_file.csv")])

    def test_invalid_csv_format(self):
        """Тест обработки некорректного CSV формата."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False, encoding="utf-8"
        ) as tmp:
            tmp.write("This is not a valid CSV format\n")

        with pytest.raises(csv.Error):
            read_csv_files([Path(tmp.name)])
