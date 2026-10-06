"""Модель SIR в долях населения: S + I + R = 1.

    dS/dt = -beta(t) * S * I
    dI/dt =  beta(t) * S * I - gamma * I
    dR/dt =  gamma * I

beta — скорость передачи, gamma = 1 / (средняя длительность болезни),
базовое репродуктивное число R0 = beta / gamma.
beta может быть функцией времени (например, карантин).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Union

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import least_squares, minimize_scalar

Beta = Union[float, Callable[[float], float]]


@dataclass(frozen=True)
class SIRResult:
    t: np.ndarray
    S: np.ndarray
    I: np.ndarray
    R: np.ndarray


def basic_r0(beta: float, gamma: float) -> float:
    if gamma <= 0:
        raise ValueError("gamma должна быть > 0")
    return beta / gamma


def simulate_sir(beta: Beta, gamma: float, i0: float = 0.01, days: float = 100,
                 steps_per_day: int = 10) -> SIRResult:
    """Решает систему SIR (solve_ivp, RK45). beta — число или функция beta(t)."""
    if not 0 < i0 < 1:
        raise ValueError("i0 — доля инфицированных, 0 < i0 < 1")
    if gamma <= 0:
        raise ValueError("gamma должна быть > 0")
    beta_fn = beta if callable(beta) else (lambda t, b=float(beta): b)

    def rhs(t, y):
        s, i, _ = y
        b = beta_fn(t)
        return [-b * s * i, b * s * i - gamma * i, gamma * i]

    t_eval = np.linspace(0, days, int(days * steps_per_day) + 1)
    sol = solve_ivp(rhs, (0, days), [1 - i0, i0, 0.0], t_eval=t_eval,
                    rtol=1e-8, atol=1e-10, max_step=1.0)
    return SIRResult(sol.t, *sol.y)


def peak(res: SIRResult) -> tuple[float, float]:
    """(день пика, доля инфицированных в пике)."""
    k = int(np.argmax(res.I))
    return float(res.t[k]), float(res.I[k])


def final_size(res: SIRResult) -> float:
    """Доля переболевших к концу моделирования."""
    return float(res.R[-1])


def fit_beta_to_peak(peak_day: float, gamma: float, i0: float,
                     days: float | None = None, bounds=(1e-3, 3.0)) -> float:
    """Подбирает beta так, чтобы пик эпидемии пришёлся на peak_day.

    Время пика убывает с ростом beta, поэтому задача одномерная.
    Это грубая калибровка по одному числу; для нескольких точек — fit_beta_to_series.
    """
    days = days or max(3 * peak_day, 60)

    def err(b):
        return abs(peak(simulate_sir(b, gamma, i0, days, steps_per_day=20))[0] - peak_day)

    return float(minimize_scalar(err, bounds=bounds, method="bounded",
                                 options={"xatol": 1e-5}).x)


def fit_beta_to_series(t_obs: np.ndarray, i_obs: np.ndarray, gamma: float,
                       i0: float | None = None, beta0: float = 0.5) -> float:
    """Подбирает beta по всему ряду наблюдений (метод наименьших квадратов).

    t_obs — моменты времени (дни), i_obs — доля инфицированных.
    i0 по умолчанию берётся из первого наблюдения.
    """
    t_obs = np.asarray(t_obs, dtype=float)
    i_obs = np.asarray(i_obs, dtype=float)
    i0 = float(i_obs[0]) if i0 is None else i0
    horizon = float(t_obs.max())

    def residuals(p):
        res = simulate_sir(p[0], gamma, i0, horizon, steps_per_day=20)
        return np.interp(t_obs, res.t, res.I) - i_obs

    return float(least_squares(residuals, [beta0], bounds=(1e-4, 5.0)).x[0])
