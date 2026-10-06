"""Синтетические RR-интервалы для демонстрации (никаких реальных пациентов)."""
from __future__ import annotations

import numpy as np


def synthetic_rr(n: int = 450, mean_rr: float = 0.8, slow_wave: float = 0.05,
                 resp_amp: float = 0.03, noise: float = 0.01, phi: float = 0.9,
                 seed: int | None = None) -> np.ndarray:
    """Модель ряда RR (секунды): среднее + медленные волны (AR(1)) +
    дыхательная аритмия (синус, ~0.25 Гц) + белый шум.

    slow_wave — амплитуда медленной AR(1)-компоненты; чем больше, тем выше C1.
    """
    rng = np.random.default_rng(seed)
    t = np.cumsum(np.full(n, mean_rr))
    slow = np.zeros(n)
    eps = rng.normal(0, slow_wave * np.sqrt(1 - phi**2), n)
    for i in range(1, n):
        slow[i] = phi * slow[i - 1] + eps[i]
    resp = resp_amp * np.sin(2 * np.pi * 0.25 * t)
    return mean_rr + slow + resp + rng.normal(0, noise, n)


def synthetic_day(seed: int = 0) -> dict[int, np.ndarray]:
    """24 часа: ночью (1–6) больше медленных волн, днём — меньше."""
    rng = np.random.default_rng(seed)
    day = {}
    for hour in range(1, 25):
        night = hour <= 6
        slow = 0.06 if night else rng.uniform(0.005, 0.04)
        day[hour] = synthetic_rr(
            n=int(rng.integers(400, 500)), slow_wave=slow,
            mean_rr=0.95 if night else 0.75, seed=int(rng.integers(1_000_000)),
        )
    return day
