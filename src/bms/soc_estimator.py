"""Coulomb-counting State-of-Charge (SOC) estimation with explicit assumptions."""
import numpy as np
import pandas as pd
from bms.load_profiles import validate_profile

def coulomb_count_soc(
    frame: pd.DataFrame,
    pack_capacity_ah: float,
    initial_soc_percent: float = 80.0,
    coulombic_efficiency: float = 1.0,
    clamp_soc: bool = False,
) -> pd.DataFrame:
    """
    Estimate SOC(%) over time via trapezoidal coulomb counting.
    Sign convention: positive current = discharge, negative current = charge.
    """
    if pack_capacity_ah <= 0:
        raise ValueError("Pack capacity must be positive.")
    if not 0.0 <= initial_soc_percent <= 100.0:
        raise ValueError("Initial SOC must be between 0 and 100%.")
    if not 0.0 < coulombic_efficiency <= 1.0:
        raise ValueError("Coulombic efficiency must be in (0, 1].")

    p = validate_profile(frame)
    t = p["time_s"].to_numpy(dtype=float)
    i = p["current_a"].to_numpy(dtype=float)

    dt = np.diff(t)
    i_avg = 0.5 * (i[:-1] + i[1:])
    # Apply coulombic efficiency during charging (negative current)
    eff = np.where(i_avg < 0.0, coulombic_efficiency, 1.0)
    delta_ah = (i_avg * eff * dt) / 3600.0
    cum_discharge_ah = np.concatenate(([0.0], np.cumsum(delta_ah)))
    soc = initial_soc_percent - 100.0 * (cum_discharge_ah / pack_capacity_ah)
    if clamp_soc:
        soc = np.clip(soc, 0.0, 100.0)

    out = p.copy()
    out["cum_discharge_ah"] = cum_discharge_ah
    out["soc_percent"] = soc
    return out
