"""Модуль с репортерами для формирования отчётов."""

from typing import Dict, Type

from src.reporters.base import BaseReporter
from src.reporters.clickbait import ClickbaitReporter

_REPORTERS: Dict[str, Type[BaseReporter]] = {
    "clickbait": ClickbaitReporter,
}


def get_reporter(report_name: str) -> Type[BaseReporter]:
    """
    Получение класса репортера по имени.

    Args:
        report_name: Имя отчёта

    Returns:
        Класс репортера

    Raises:
        ValueError: Если отчёт с таким именем не зарегистрирован
    """
    if report_name not in _REPORTERS:
        raise ValueError(f"Неизвестный тип отчёта: {report_name}")
    return _REPORTERS[report_name]


def register_reporter(name: str, reporter_class: Type[BaseReporter]) -> None:
    """
    Регистрация нового репортера.

    Args:
        name: Имя отчёта
        reporter_class: Класс репортера
    """
    _REPORTERS[name] = reporter_class
