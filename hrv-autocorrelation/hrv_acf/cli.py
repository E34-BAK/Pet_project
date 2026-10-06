"""Командная строка: python -m hrv_acf.cli data.csv [--column rr]"""
from __future__ import annotations

import argparse

import pandas as pd

from .core import analyze_hours


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="C1/C0 по часам из CSV (колонки: hour, rr)")
    p.add_argument("csv")
    p.add_argument("--hour-col", default="hour")
    p.add_argument("--rr-col", default="rr")
    p.add_argument("--method", choices=["pearson", "standard"], default="pearson")
    a = p.parse_args(argv)

    df = pd.read_csv(a.csv)
    hours = {int(h): g[a.rr_col].dropna().to_numpy() for h, g in df.groupby(a.hour_col)}
    print(f"{'Час':<5}{'N':<7}{'C1':<10}{'C0':<8}Интерпретация")
    for r in analyze_hours(hours, a.method):
        c1 = "—" if r.c1 is None else f"{r.c1:.3f}"
        c0 = "нет" if r.c0 is None else str(r.c0)
        print(f"{r.hour:<5}{r.n:<7}{c1:<10}{c0:<8}{r.interpretation}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
