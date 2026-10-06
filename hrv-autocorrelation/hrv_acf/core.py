"""Автокорреляционный анализ RR-интервалов.

C1 — коэффициент автокорреляции при лаге 1.
C0 — номер первого лага, на котором автокорреляция становится отрицательной
     (None, если отрицательных значений нет).

Метод основан на учебной методичке по анализу вариабельности сердечного ритма;
пороги интерпретации C1 — учебные, это НЕ клинический инструмент.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional, Sequence

import numpy as np

MIN_POINTS = 10


def _clean(series: Iterable[float]) -> np.ndarray:
    x = np.asarray(list(series), dtype=float)
    return x[~np.isnan(x)]


def autocorrelation(series: Iterable[float], max_lag: Optional[int] = None,
                    method: str = "pearson") -> np.ndarray:
    """Автокорреляционная функция для лагов 0..max_lag.

    Параметры
    ---------
    series : RR-интервалы (NaN отбрасываются).
    max_lag : максимальный лаг; по умолчанию и максимум — len(series) // 4.
    method : "pearson" — коэффициент Пирсона между x[lag:] и x[:-lag]
             (как в учебной методичке);
             "standard" — классическая оценка ACF (нормировка на общую дисперсию).

    Возвращает массив длины max_lag + 1, acf[0] == 1.
    Для постоянного ряда возвращает нули (кроме лага 0), а не NaN.
    """
    x = _clean(series)
    n = len(x)
    if n < MIN_POINTS:
        raise ValueError(f"Нужно минимум {MIN_POINTS} значений, получено {n}")
    limit = n // 4
    max_lag = limit if max_lag is None else min(int(max_lag), limit)
    if max_lag < 1:
        raise ValueError("max_lag должен быть >= 1")

    acf = np.zeros(max_lag + 1)
    acf[0] = 1.0

    if method == "pearson":
        for lag in range(1, max_lag + 1):
            a, b = x[lag:], x[:-lag]
            if a.std() == 0 or b.std() == 0:
                acf[lag] = 0.0
            else:
                acf[lag] = np.corrcoef(a, b)[0, 1]
    elif method == "standard":
        d = x - x.mean()
        denom = float(np.dot(d, d))
        if denom == 0:
            return acf
        for lag in range(1, max_lag + 1):
            acf[lag] = float(np.dot(d[lag:], d[:-lag])) / denom
    else:
        raise ValueError("method должен быть 'pearson' или 'standard'")
    return acf


def c1_c0(series: Iterable[float], method: str = "pearson"):
    """Возвращает (C1, C0). Для слишком короткого ряда — (None, None)."""
    x = _clean(series)
    if len(x) < MIN_POINTS:
        return None, None
    acf = autocorrelation(x, method=method)
    c1 = float(acf[1])
    negatives = np.flatnonzero(acf[1:] < 0)
    c0 = int(negatives[0] + 1) if negatives.size else None
    return c1, c0


def interpret_c1(c1: Optional[float]) -> str:
    """Словесная оценка C1 (учебные пороги)."""
    if c1 is None:
        return "Недостаточно данных"
    if c1 > 0.9:
        return "Очень высокая корреляция (медленные волны)"
    if c1 > 0.7:
        return "Высокая корреляция"
    if c1 > 0.5:
        return "Средняя корреляция"
    if c1 > 0.3:
        return "Низкая корреляция"
    if c1 > 0:
        return "Очень низкая корреляция"
    return "Отрицательная корреляция"


@dataclass(frozen=True)
class HourResult:
    hour: int
    n: int
    c1: Optional[float]
    c0: Optional[int]
    interpretation: str


def analyze_hours(hours: dict[int, Sequence[float]], method: str = "pearson") -> list[HourResult]:
    """Считает C1 и C0 для каждого часа суток.

    hours — словарь {номер часа: RR-интервалы этого часа}.
    """
    results = []
    for hour in sorted(hours):
        data = _clean(hours[hour])
        c1, c0 = c1_c0(data, method=method)
        results.append(HourResult(hour, len(data), c1, c0, interpret_c1(c1)))
    return results
