"""Демо: суточный анализ на синтетических данных. Запуск из папки проекта:
    python examples/demo.py
Сохраняет графики в docs/."""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from hrv_acf import analyze_hours, autocorrelation, synthetic_day, synthetic_rr  # noqa: E402

docs = ROOT / "docs"
docs.mkdir(exist_ok=True)

# 1. Коррелограмма одного часа
rr = synthetic_rr(n=450, slow_wave=0.05, seed=1)
acf = autocorrelation(rr)
fig, ax = plt.subplots(figsize=(8, 3.5))
ax.stem(range(len(acf)), acf, basefmt=" ")
ax.axhline(0, color="r", ls="--", lw=0.8)
ax.set(xlabel="Лаг", ylabel="Автокорреляция", title="Коррелограмма (синтетический ряд RR)")
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(docs / "correlogram.png", dpi=130)

# 2. Суточная динамика C1 и C0
res = analyze_hours(synthetic_day(seed=0))
hours = [r.hour for r in res]
fig, (a1, a2) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
a1.plot(hours, [r.c1 for r in res], "o-")
a1.set(ylabel="C1", title="Суточная динамика C1 и C0 (синтетические данные)")
a2.plot(hours, [r.c0 if r.c0 is not None else float("nan") for r in res], "s-", color="tab:green")
a2.set(ylabel="C0 (лаг)", xlabel="Час")
for a in (a1, a2):
    a.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(docs / "daily_c1_c0.png", dpi=130)

print(f"{'Час':<5}{'N':<6}{'C1':<8}{'C0':<6}Интерпретация")
for r in res:
    print(f"{r.hour:<5}{r.n:<6}{r.c1:<8.3f}{str(r.c0 or '—'):<6}{r.interpretation}")
