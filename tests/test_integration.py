"""Интеграционные тесты с использованием fixture файлов."""

import pytest
from pathlib import Path

from src.cli import validate_files
from src.utils import read_csv_files
from src.reporters.clickbait import ClickbaitReporter


class TestIntegration:
    """Интеграционные тесты."""

    @pytest.fixture
    def fixtures_dir(self) -> Path:
        """Путь к директории с фикстурами."""
        return Path(__file__).parent / "fixtures"

    def test_read_valid_data_file(self, fixtures_dir: Path):
        """Тест чтения валидного файла с данными."""
        file_path = fixtures_dir / "valid_data.csv"
        data = read_csv_files([file_path])
        
        assert len(data) == 10
        assert data[0]["title"] == "Я бросил IT и стал фермером"
        assert data[0]["ctr"] == "18.2"
        assert data[0]["retention_rate"] == "35"

    def test_read_empty_data_file(self, fixtures_dir: Path):
        """Тест чтения пустого файла (только заголовки)."""
        file_path = fixtures_dir / "empty_data.csv"
        data = read_csv_files([file_path])
        
        assert len(data) == 0

    def test_clickbait_report_with_fixture_data(self, fixtures_dir: Path):
        """Тест формирования отчёта на основе fixture данных."""
        file_path = fixtures_dir / "valid_data.csv"
        data = read_csv_files([file_path])
        
        reporter = ClickbaitReporter()
        result = reporter.generate(data)
        
        # Ожидаемые кликбейтные видео из файла
        expected_titles = [
            "Секрет который скрывают тимлиды",
            "Как я спал по 4 часа и ничего не понял",
            "Как я задолжал ревьюеру 1000 строк кода",
            "Купил джуну макбук и он уволился",
            "Я бросил IT и стал фермером",
        ]
        
        assert len(result) == 5
        assert [item["title"] for item in result] == expected_titles
        
        # Проверка значений
        assert result[0]["ctr"] == 25
        assert result[0]["retention_rate"] == 22
        
        assert result[-1]["ctr"] == 18.2
        assert result[-1]["retention_rate"] == 35

    def test_full_integration_flow(self, fixtures_dir: Path, capsys):
        """Тест полного интеграционного сценария."""
        from src.cli import main as cli_main
        from unittest.mock import patch
        
        file_path = str(fixtures_dir / "valid_data.csv")
        
        with patch("sys.argv", ["main.py", "--files", file_path, "--report", "clickbait"]):
            cli_main()
        
        captured = capsys.readouterr()
        
        # Проверяем, что в выводе есть ожидаемые видео
        assert "Секрет который скрывают тимлиды" in captured.out
        assert "25" in captured.out
        assert "22" in captured.out
        assert "Как я спал по 4 часа и ничего не понял" in captured.out
        assert "22.5" in captured.out

    def test_multiple_files_integration(self, fixtures_dir: Path, tmp_path: Path):
        """Тест обработки нескольких файлов."""
        # Создаем дополнительный тестовый файл
        extra_file = tmp_path / "extra_data.csv"
        extra_file.write_text(
            "title,ctr,retention_rate\n"
            "Дополнительное видео,30.0,25\n"
            "Обычное видео,10.0,50\n"
        )
        
        data1 = read_csv_files([fixtures_dir / "valid_data.csv"])
        data2 = read_csv_files([extra_file])
        
        all_data = data1 + data2
        
        reporter = ClickbaitReporter()
        result = reporter.generate(all_data)
        
        # Проверяем, что данные из обоих файлов обработаны
        titles = [item["title"] for item in result]
        assert "Секрет который скрывают тимлиды" in titles
        assert "Дополнительное видео" in titles
        assert "Обычное видео" not in titles
