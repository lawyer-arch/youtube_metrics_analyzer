"""Тесты для репортеров."""

import pytest

from src.reporters.clickbait import ClickbaitReporter
from src.reporters.base import BaseReporter


class TestClickbaitReporter:
    """Тесты для ClickbaitReporter."""

    @pytest.fixture
    def reporter(self) -> ClickbaitReporter:
        """Фикстура репортера."""
        return ClickbaitReporter()

    @pytest.fixture
    def sample_data(self) -> list:
        """Фикстура с тестовыми данными."""
        return [
            {"title": "Video 1", "ctr": "20.5", "retention_rate": "35"},
            {"title": "Video 2", "ctr": "18.2", "retention_rate": "28"},
            {"title": "Video 3", "ctr": "25.0", "retention_rate": "22"},
            {"title": "Video 4", "ctr": "10.0", "retention_rate": "30"},  # низкий CTR
            {"title": "Video 5", "ctr": "30.0", "retention_rate": "45"},  # высокое удержание
            {"title": "Video 6", "ctr": "16.0", "retention_rate": "50"},  # высокое удержание
            {"title": "Video 7", "ctr": "14.0", "retention_rate": "38"},  # низкий CTR
        ]

    def test_filter_clickbait_videos(self, reporter: ClickbaitReporter, sample_data: list):
        """Тест фильтрации кликбейтных видео."""
        result = reporter.generate(sample_data)

        # Должны попасть видео с CTR > 15 и retention < 40
        # Video 1 (20.5, 35), Video 2 (18.2, 28), Video 3 (25.0, 22)
        assert len(result) == 3
        titles = [item["title"] for item in result]
        assert "Video 1" in titles
        assert "Video 2" in titles
        assert "Video 3" in titles
        assert "Video 4" not in titles
        assert "Video 5" not in titles
        assert "Video 6" not in titles
        assert "Video 7" not in titles

    def test_sorting_by_ctr_desc(self, reporter: ClickbaitReporter, sample_data: list):
        """Тест сортировки по убыванию CTR."""
        result = reporter.generate(sample_data)

        # Проверяем порядок: Video 3 (25.0), Video 1 (20.5), Video 2 (18.2)
        assert result[0]["title"] == "Video 3"
        assert result[1]["title"] == "Video 1"
        assert result[2]["title"] == "Video 2"

        # Проверяем значения CTR
        ctr_values = [item["ctr"] for item in result]
        assert ctr_values == [25.0, 20.5, 18.2]

    def test_empty_data(self, reporter: ClickbaitReporter):
        """Тест с пустыми данными."""
        result = reporter.generate([])
        assert result == []

    def test_no_matching_videos(self, reporter: ClickbaitReporter):
        """Тест когда нет видео подходящих под условия."""
        data = [
            {"title": "Low CTR", "ctr": "10", "retention_rate": "30"},
            {"title": "High Retention", "ctr": "20", "retention_rate": "80"},
            {"title": "Borderline CTR", "ctr": "15", "retention_rate": "39"},
            {"title": "Borderline Retention", "ctr": "16", "retention_rate": "40"},
        ]
        result = reporter.generate(data)
        assert result == []

    def test_invalid_numeric_values(self, reporter: ClickbaitReporter):
        """Тест с некорректными числовыми значениями."""
        data = [
            {"title": "Valid", "ctr": "20", "retention_rate": "30"},
            {"title": "Invalid CTR", "ctr": "invalid", "retention_rate": "30"},
            {"title": "Invalid Retention", "ctr": "20", "retention_rate": "invalid"},
            {"title": "Missing Fields", "ctr": "20"},
            {"title": "Empty Values", "ctr": "", "retention_rate": ""},
        ]
        result = reporter.generate(data)

        # Только валидная строка должна попасть в результат
        assert len(result) == 1
        assert result[0]["title"] == "Valid"

    def test_mixed_data_types(self, reporter: ClickbaitReporter):
        """Тест со смешанными типами данных."""
        data = [
            {"title": "String CTR", "ctr": "25.5", "retention_rate": "35"},
            {"title": "Float CTR", "ctr": 22.3, "retention_rate": 30},
            {"title": "Int CTR", "ctr": 18, "retention_rate": 28},
        ]
        result = reporter.generate(data)
        assert len(result) == 3

    def test_get_headers(self, reporter: ClickbaitReporter):
        """Тест получения заголовков."""
        headers = reporter.get_headers()
        assert headers == ["title", "ctr", "retention_rate"]

    def test_inheritance(self):
        """Тест наследования от базового класса."""
        assert issubclass(ClickbaitReporter, BaseReporter)
        reporter = ClickbaitReporter()
        assert isinstance(reporter, BaseReporter)
