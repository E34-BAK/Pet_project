"""Математические модели биосистем: SIR и модели роста популяции."""
from .sir import (SIRResult, simulate_sir, basic_r0, peak, final_size,
                  fit_beta_to_peak, fit_beta_to_series)
from .growth import (malthus, verhulst, doubling_time, fit_malthus, fit_verhulst)

__all__ = [
    "SIRResult", "simulate_sir", "basic_r0", "peak", "final_size",
    "fit_beta_to_peak", "fit_beta_to_series",
    "malthus", "verhulst", "doubling_time", "fit_malthus", "fit_verhulst",
]
