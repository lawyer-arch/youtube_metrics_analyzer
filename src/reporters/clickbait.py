"""Репортер для поиска кликбейтных видео."""

from typing import List, Dict, Any

from src.reporters.base import BaseReporter


class ClickbaitReporter(BaseReporter):
    """
    Репортер для отбора кликбейтных видео.

    Условия:
    - CTR > 15%
    - Удержание < 40%
    """

    def generate(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Отбор видео с высоким CTR и низким удержанием.

        Результат сортируется по убыванию CTR.
        """
        filtered = []

        for row in data:
            try:
                ctr = float(row.get("ctr", 0))
                retention = float(row.get("retention_rate", 0))

                if ctr > 15 and retention < 40:
                    filtered.append(
                        {
                            "title": row.get("title", ""),
                            "ctr": ctr,
                            "retention_rate": retention,
                        }
                    )
            except (ValueError, TypeError):
                # Пропускаем строки с некорректными данными
                continue

        # Сортировка по убыванию CTR
        filtered.sort(key=lambda x: x["ctr"], reverse=True)

        return filtered

    def get_headers(self) -> List[str]:
        """Возвращает заголовки для таблицы."""
        return ["title", "ctr", "retention_rate"]
