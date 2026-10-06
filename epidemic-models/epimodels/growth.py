"""Модели роста популяции: Мальтус (экспонента) и Ферхюльст (логистика)."""
from __future__ import annotations

import numpy as np
from scipy.optimize import curve_fit


def malthus(t, n0: float, r: float):
    """N(t) = N0 * exp(r t)."""
    return n0 * np.exp(r * np.asarray(t, dtype=float))


def verhulst(t, n0: float, r: float, k: float):
    """Логистический рост: N(t) = K N0 e^{rt} / (K + N0 (e^{rt} - 1))."""
    e = np.exp(r * np.asarray(t, dtype=float))
    return k * n0 * e / (k + n0 * (e - 1))


def doubling_time(r: float) -> float:
    """Время удвоения ln2 / r (для r < 0 — время уменьшения вдвое)."""
    if r == 0:
        raise ValueError("при r = 0 численность не меняется")
    return float(np.log(2) / abs(r))


def fit_malthus(t, n):
    """Линейная регрессия ln N = ln N0 + r t. Возвращает (N0, r, R2 по ln N)."""
    t = np.asarray(t, dtype=float)
    ln_n = np.log(np.asarray(n, dtype=float))
    r, ln_n0 = np.polyfit(t, ln_n, 1)
    pred = ln_n0 + r * t
    ss_res = float(np.sum((ln_n - pred) ** 2))
    ss_tot = float(np.sum((ln_n - ln_n.mean()) ** 2))
    return float(np.exp(ln_n0)), float(r), 1 - ss_res / ss_tot


def fit_verhulst(t, n):
    """Подбор (N0, r, K) нелинейным МНК. Возвращает (N0, r, K)."""
    t = np.asarray(t, dtype=float)
    n = np.asarray(n, dtype=float)
    p0 = [n[0], 0.05, n.max() * 1.5]
    popt, _ = curve_fit(verhulst, t, n, p0=p0,
                        bounds=([0, -1, n.max() * 0.5], [np.inf, 5, np.inf]), maxfev=20000)
    return tuple(float(v) for v in popt)
