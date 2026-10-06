"""Демо: python examples/demo.py  (графики сохраняются в docs/)."""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from epimodels import (basic_r0, doubling_time, fit_beta_to_peak, fit_beta_to_series,  # noqa: E402
                       fit_malthus, fit_verhulst, malthus, peak, simulate_sir, verhulst)

docs = ROOT / "docs"
docs.mkdir(exist_ok=True)

# 1. Влияние beta
fig, ax = plt.subplots(figsize=(8, 4.5))
for b in (0.15, 0.3, 0.5):
    r = simulate_sir(b, 0.1, i0=0.01, days=120)
    d, p = peak(r)
    ax.plot(r.t, r.I * 100, label=f"β={b}, R0={basic_r0(b, 0.1):.1f}, пик на {d:.0f}-й день")
ax.set(xlabel="Дни", ylabel="Инфицированные, %", title="SIR: влияние скорости передачи β")
ax.legend(); ax.grid(alpha=0.3); fig.tight_layout(); fig.savefig(docs / "sir_beta.png", dpi=130)

# 2. Карантин: beta падает вдвое с 10 по 50 день
quarantine = lambda t: 0.15 if 10 <= t <= 50 else 0.3
base = simulate_sir(0.3, 0.1, 0.01, 120)
q = simulate_sir(quarantine, 0.1, 0.01, 120)
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.plot(base.t, base.I * 100, label="без карантина")
ax.plot(q.t, q.I * 100, label="карантин (β×0.5, дни 10–50)")
ax.set(xlabel="Дни", ylabel="Инфицированные, %", title="SIR: эффект карантина")
ax.legend(); ax.grid(alpha=0.3); fig.tight_layout(); fig.savefig(docs / "sir_quarantine.png", dpi=130)

# 3. Калибровка beta по синтетическим «наблюдениям» (недельные данные с шумом)
gamma, true_beta = 1 / 7, 0.45
truth = simulate_sir(true_beta, gamma, 0.002, 168)
weeks = np.arange(0, 169, 7)
rng = np.random.default_rng(0)
obs = np.interp(weeks, truth.t, truth.I) * (1 + rng.normal(0, 0.05, len(weeks)))
b_series = fit_beta_to_series(weeks, obs, gamma, i0=0.002)
b_peak = fit_beta_to_peak(weeks[np.argmax(obs)], gamma, 0.002)
print(f"истинное β={true_beta}; по всему ряду β={b_series:.3f}; по дню пика β={b_peak:.3f}; R0={b_series/gamma:.2f}")
fit = simulate_sir(b_series, gamma, 0.002, 168)
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.plot(weeks, obs * 100, "o", label="наблюдения (синтетические)")
ax.plot(fit.t, fit.I * 100, label=f"SIR, β={b_series:.3f}, R0={b_series/gamma:.2f}")
ax.set(xlabel="Дни", ylabel="Инфицированные, %", title="Калибровка β методом наименьших квадратов")
ax.legend(); ax.grid(alpha=0.3); fig.tight_layout(); fig.savefig(docs / "sir_fit.png", dpi=130)

# 4. Мальтус и Ферхюльст на синтетическом ряду
years = np.arange(0, 60)
pop = verhulst(years, 5e6, 0.07, 6e7) * (1 + rng.normal(0, 0.01, len(years)))
n0m, rm, r2 = fit_malthus(years, pop)
n0v, rv, kv = fit_verhulst(years, pop)
print(f"Мальтус: r={rm:.4f}, R2(ln)={r2:.3f}, время удвоения {doubling_time(rm):.1f}")
print(f"Ферхюльст: r={rv:.4f}, K={kv:.3g}")
fut = np.arange(0, 100)
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.plot(years, pop, ".", label="данные (синтетические)")
ax.plot(fut, malthus(fut, n0m, rm), "--", label=f"Мальтус r={rm:.3f}")
ax.plot(fut, verhulst(fut, n0v, rv, kv), label=f"Ферхюльст r={rv:.3f}, K={kv:.2g}")
ax.set(ylim=(0, kv * 1.3), xlabel="Годы", ylabel="Численность", title="Рост популяции: экспонента и логистика")
ax.legend(); ax.grid(alpha=0.3); fig.tight_layout(); fig.savefig(docs / "growth.png", dpi=130)
