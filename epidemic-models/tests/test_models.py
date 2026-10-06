import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from epimodels import (basic_r0, doubling_time, final_size, fit_beta_to_peak,  # noqa: E402
                       fit_beta_to_series, fit_malthus, fit_verhulst, malthus, peak,
                       simulate_sir, verhulst)


def test_population_conserved():
    r = simulate_sir(0.4, 0.1, 0.01, 100)
    assert np.allclose(r.S + r.I + r.R, 1.0, atol=1e-6)


def test_r0_below_one_no_epidemic():
    r = simulate_sir(0.05, 0.1, 0.01, 200)  # R0 = 0.5
    assert r.I[-1] < r.I[0] and peak(r)[0] == 0


def test_r0_above_one_has_interior_peak():
    r = simulate_sir(0.3, 0.1, 0.01, 200)
    day, val = peak(r)
    assert day > 0 and val > 0.01


def test_higher_beta_earlier_and_higher_peak():
    a = peak(simulate_sir(0.2, 0.1, 0.01, 200))
    b = peak(simulate_sir(0.5, 0.1, 0.01, 200))
    assert b[0] < a[0] and b[1] > a[1]


def test_final_size_matches_theory():
    # итоговый размер z решает z = 1 - exp(-R0 z) (при малом i0)
    b, g = 0.3, 0.1
    z = final_size(simulate_sir(b, g, 1e-6, 400))
    assert z == pytest.approx(1 - np.exp(-(b / g) * z), abs=1e-3)


def test_quarantine_reduces_peak():
    base = peak(simulate_sir(0.3, 0.1, 0.01, 150))[1]
    q = peak(simulate_sir(lambda t: 0.15 if 10 <= t <= 50 else 0.3, 0.1, 0.01, 150))[1]
    assert q < base


def test_invalid_input():
    with pytest.raises(ValueError):
        simulate_sir(0.3, 0.0)
    with pytest.raises(ValueError):
        simulate_sir(0.3, 0.1, i0=1.5)
    with pytest.raises(ValueError):
        basic_r0(0.3, 0)


def test_fit_beta_from_series_recovers_truth():
    gamma, beta, i0 = 1 / 7, 0.45, 0.002
    truth = simulate_sir(beta, gamma, i0, 168)
    t = np.arange(0, 169, 7)
    obs = np.interp(t, truth.t, truth.I)
    assert fit_beta_to_series(t, obs, gamma, i0) == pytest.approx(beta, rel=0.02)


def test_fit_beta_to_peak_hits_target_day():
    gamma, i0 = 1 / 7, 0.002
    beta = fit_beta_to_peak(60, gamma, i0)
    day = peak(simulate_sir(beta, gamma, i0, 180, steps_per_day=20))[0]
    assert day == pytest.approx(60, abs=1.0)


def test_malthus_doubling_time():
    r = 0.07
    t2 = doubling_time(r)
    assert malthus(t2, 100, r) == pytest.approx(200)
    assert doubling_time(-r) == pytest.approx(t2)


def test_fit_malthus_recovers_parameters():
    t = np.arange(30)
    n0, r, r2 = fit_malthus(t, malthus(t, 120, 0.03))
    assert n0 == pytest.approx(120, rel=1e-6) and r == pytest.approx(0.03) and r2 > 0.999999


def test_fit_verhulst_recovers_parameters():
    t = np.arange(80)
    n0, r, k = fit_verhulst(t, verhulst(t, 1e6, 0.1, 2e7))
    assert (n0, r, k) == pytest.approx((1e6, 0.1, 2e7), rel=0.02)


def test_verhulst_saturates_at_k():
    assert verhulst(1000, 10, 0.2, 500) == pytest.approx(500, rel=1e-6)
