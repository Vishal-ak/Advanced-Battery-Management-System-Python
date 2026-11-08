"""Load profile generation and basic current/charge/energy accounting."""
import numpy as np
import pandas as pd

def _validate_duration(duration_s: float, dt_s: float) -> None:
    if duration_s <= 0 or dt_s <= 0:
        raise ValueError("Duration and time step must be positive.")
    if dt_s > duration_s:
        raise ValueError("Time step cannot exceed duration.")

def constant_profile(current_a: float, duration_s: float, dt_s: float = 1.0) -> pd.DataFrame:
    _validate_duration(duration_s, dt_s)
    t = np.arange(0, duration_s + dt_s * 0.5, dt_s)
    t = t[t <= duration_s + 1e-12]
    return pd.DataFrame({"time_s": t, "current_a": np.full(t.size, float(current_a))})

def step_profile(low_a: float, high_a: float, step_at_s: float,
                 duration_s: float, dt_s: float = 1.0) -> pd.DataFrame:
    _validate_duration(duration_s, dt_s)
    if not 0 <= step_at_s <= duration_s:
        raise ValueError("Step time must lie within the profile duration.")
    t = np.arange(0, duration_s + dt_s * 0.5, dt_s)
    t = t[t <= duration_s + 1e-12]
    return pd.DataFrame({"time_s": t, "current_a": np.where(t < step_at_s, float(low_a), float(high_a))})

def pulse_profile(peak_a: float, pulse_s: float, rest_s: float,
                  cycles: int = 3, dt_s: float = 1.0) -> pd.DataFrame:
    if pulse_s <= 0 or rest_s < 0 or cycles < 1 or dt_s <= 0:
        raise ValueError("Pulse duration and time step must be positive; rest non-negative; cycles >= 1.")
    duration = cycles * (pulse_s + rest_s)
    t = np.arange(0, duration + dt_s * 0.5, dt_s)
    t = t[t <= duration + 1e-12]
    phase = np.mod(t, pulse_s + rest_s)
    current = np.where(phase < pulse_s, float(peak_a), 0.0)
    return pd.DataFrame({"time_s": t, "current_a": current})

def validate_profile(frame: pd.DataFrame) -> pd.DataFrame:
    if not {"time_s", "current_a"}.issubset(frame.columns):
        raise ValueError("CSV/profile must contain time_s and current_a columns.")
    out = frame[["time_s", "current_a"]].copy()
    out = out.apply(pd.to_numeric, errors="raise")
    if len(out) < 2 or not np.isfinite(out.to_numpy()).all():
        raise ValueError("Profile needs at least two finite samples.")
    t = out["time_s"].to_numpy()
    if np.any(np.diff(t) <= 0):
        raise ValueError("time_s must be strictly increasing.")
    return out

def _trapz(y: np.ndarray, x: np.ndarray) -> float:
    return float(np.trapezoid(y, x)) if hasattr(np, "trapezoid") else float(np.trapz(y, x))

def profile_metrics(frame: pd.DataFrame, pack_capacity_ah: float,
                    pack_nominal_voltage_v: float) -> dict:
    if pack_capacity_ah <= 0 or pack_nominal_voltage_v <= 0:
        raise ValueError("Pack capacity and nominal voltage must be positive.")
    p = validate_profile(frame)
    t = p.time_s.to_numpy()
    i = p.current_a.to_numpy()
    # Positive current denotes discharge; negative current denotes charging.
    charge_ah = _trapz(i, t) / 3600.0
    abs_throughput_ah = _trapz(np.abs(i), t) / 3600.0
    return {
        "duration_s": float(t[-1] - t[0]),
        "peak_discharge_current_a": float(max(0.0, i.max())),
        "peak_charge_current_a": float(max(0.0, -i.min())),
        "net_discharge_ah": charge_ah,
        "absolute_throughput_ah": abs_throughput_ah,
        "net_soc_change_percent": float(-100.0 * charge_ah / pack_capacity_ah),
        "nominal_energy_throughput_wh": float(abs_throughput_ah * pack_nominal_voltage_v),
        "peak_c_rate": float(max(abs(i.max()), abs(i.min())) / pack_capacity_ah),
    }
