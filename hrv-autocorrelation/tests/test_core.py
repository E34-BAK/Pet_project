import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from hrv_acf import analyze_hours, autocorrelation, c1_c0, interpret_c1, synthetic_rr  # noqa: E402


def test_lag0_is_one_and_length():
    acf = autocorrelation(np.random.default_rng(0).normal(size=200), max_lag=20)
    assert acf[0] == 1.0 and len(acf) == 21


def test_max_lag_capped_at_quarter():
    acf = autocorrelation(np.arange(40.0) % 7, max_lag=1000)
    assert len(acf) == 40 // 4 + 1


def test_white_noise_c1_near_zero():
    x = np.random.default_rng(1).normal(size=5000)
    c1, _ = c1_c0(x)
    assert abs(c1) < 0.05


def test_ar1_c1_matches_phi():
    rng = np.random.default_rng(2)
    phi, n = 0.9, 20000
    x = np.zeros(n)
    e = rng.normal(size=n)
    for i in range(1, n):
        x[i] = phi * x[i - 1] + e[i]
    c1, _ = c1_c0(x)
    assert c1 == pytest.approx(phi, abs=0.02)


def test_sine_first_negative_lag():
    period = 40
    x = np.sin(2 * np.pi * np.arange(400) / period)
    _, c0 = c1_c0(x)
    # первый отрицательный лаг у синуса — чуть больше четверти периода
    assert c0 in range(period // 4, period // 4 + 3)


def test_constant_series_has_no_nan():
    acf = autocorrelation(np.ones(50))
    assert not np.isnan(acf).any() and acf[1] == 0.0


def test_too_short_series():
    assert c1_c0([1, 2, 3]) == (None, None)
    with pytest.raises(ValueError):
        autocorrelation([1, 2, 3])


def test_nan_values_are_dropped():
    x = synthetic_rr(300, seed=3)
    x_nan = np.insert(x, [10, 50], np.nan)
    assert np.allclose(autocorrelation(x), autocorrelation(x_nan))


def test_methods_agree_on_long_series():
    x = synthetic_rr(2000, seed=4)
    p = autocorrelation(x, max_lag=10, method="pearson")
    s = autocorrelation(x, max_lag=10, method="standard")
    assert np.allclose(p, s, atol=0.05)


def test_more_slow_waves_higher_c1():
    low = c1_c0(synthetic_rr(450, slow_wave=0.002, seed=5))[0]
    high = c1_c0(synthetic_rr(450, slow_wave=0.08, seed=5))[0]
    assert high > low


def test_interpretation_thresholds():
    assert interpret_c1(0.95).startswith("Очень высокая")
    assert interpret_c1(0.8) == "Высокая корреляция"
    assert interpret_c1(-0.1) == "Отрицательная корреляция"
    assert interpret_c1(None) == "Недостаточно данных"


def test_analyze_hours_structure():
    res = analyze_hours({1: synthetic_rr(300, seed=6), 2: [1, 2, 3]})
    assert [r.hour for r in res] == [1, 2]
    assert res[1].c1 is None and res[0].c1 is not None
