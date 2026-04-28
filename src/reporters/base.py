"""Базовый класс для всех репортеров."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseReporter(ABC):
    """Абстрактный базовый класс для формирования отчётов."""

    @abstractmethod
    def generate(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Генерация отчёта на основе данных.

        Args:
            data: Список словарей с данными из CSV файлов

        Returns:
            Список словарей с отфильтрованными и отсортированными данными
        """
        pass

    @abstractmethod
    def get_headers(self) -> List[str]:
        """
        Получение заголовков таблицы для вывода.

        Returns:
            Список названий колонок для отображения
        """
        pass
