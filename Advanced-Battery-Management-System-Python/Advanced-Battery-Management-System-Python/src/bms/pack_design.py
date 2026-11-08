"""Transparent first-order series/parallel battery pack calculations."""
from dataclasses import dataclass, asdict
from typing import Optional

@dataclass(frozen=True)
class PackResult:
    series_cells: int
    parallel_cells: int
    total_cells: int
    nominal_voltage_v: float
    maximum_voltage_v: Optional[float]
    cutoff_voltage_v: Optional[float]
    capacity_ah: float
    nominal_energy_wh: float
    nominal_energy_kwh: float
    total_mass_kg: Optional[float]

def design_pack(cell: dict, series: int, parallel: int) -> PackResult:
    if isinstance(series, bool) or isinstance(parallel, bool):
        raise TypeError("Series and parallel counts must be integers.")
    if not isinstance(series, int) or not isinstance(parallel, int):
        raise TypeError("Series and parallel counts must be integers.")
    if series < 1 or parallel < 1:
        raise ValueError("Series and parallel counts must be positive integers.")
    required = ("nominal_voltage_v", "capacity_ah_typ")
    if any(cell.get(k) is None or cell[k] <= 0 for k in required):
        raise ValueError("Cell nominal voltage and typical capacity must be positive.")

    n = series * parallel
    vmax = cell.get("charge_voltage_v")
    vcut = cell.get("discharge_cutoff_v")
    mass = cell.get("mass_g_max")
    vnom = series * cell["nominal_voltage_v"]
    cap = parallel * cell["capacity_ah_typ"]
    energy = vnom * cap

    return PackResult(
        series_cells=series,
        parallel_cells=parallel,
        total_cells=n,
        nominal_voltage_v=vnom,
        maximum_voltage_v=series * vmax if vmax is not None else None,
        cutoff_voltage_v=series * vcut if vcut is not None else None,
        capacity_ah=cap,
        nominal_energy_wh=energy,
        nominal_energy_kwh=energy / 1000.0,
        total_mass_kg=n * mass / 1000.0 if mass is not None else None,
    )

def pack_summary(result: PackResult) -> dict:
    return asdict(result)
