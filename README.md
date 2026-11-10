# Advanced Battery Management System — Python

An independently structured Python engineering workbench for EV/HEV lithium-ion battery pack sizing, time-domain current-profile analysis and coulomb-counting SOC.

> **Scope:** research and educational software, not a production BMS or safety controller. ECM voltage prediction and thermal prediction are deliberately deferred until suitable cell-specific parameters and validation evidence are available.

## Features
- Manufacturer specification catalogue: Panasonic NCR18650B, LG INR18650 MJ1 and Molicel INR-18650-P28A.
- Series/parallel pack voltage, capacity, energy and cell-only mass calculations.
- Constant, step and pulse current-profile generation.
- CSV current profile import (`time_s,current_a`).
- Peak current, C-rate, net Ah, absolute Ah throughput and nominal-voltage energy-throughput estimates.
- Coulomb-counting SOC with explicit current sign convention and charge efficiency.
- Streamlit dashboard, Plotly charts, CSV downloads and automated tests.

## Quick start

```bash
git clone https://github.com/Vishal-ak/Advanced-Battery-Management-System-Python.git
cd Advanced-Battery-Management-System-Python
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

Run checks:

```bash
python -m pytest -q
python -m compileall -q .
```

## Project structure

```text
.
├── app.py
├── requirements.txt
├── .gitignore
├── README.md
├── src/bms/
│   ├── __init__.py
│   ├── cell_library.py
│   ├── pack_design.py
│   ├── load_profiles.py
│   └── soc_estimator.py
├── tests/
│   ├── test_pack_design.py
│   ├── test_load_profiles.py
│   └── test_soc_estimator.py
└── docs/
    ├── DATA_SOURCES.md
    ├── MODEL_SCOPE.md
    ├── SYSTEM_ARCHITECTURE.md
    ├── VALIDATION_PLAN.md
    └── USER_GUIDE.md
```

## Engineering conventions
- Positive current = battery discharge; negative current = battery charging.
- Pack calculations assume identical cells and ideal interconnections.
- Nominal energy is nominal pack voltage × pack capacity.
- Energy throughput uses absolute Ah throughput × nominal pack voltage; it is not measured terminal energy.
- Mass is cell-only and excludes pack hardware.
- Missing specification values remain `None`; values are not inferred from another cell.
- SOC is calculated by trapezoidal coulomb counting. Charging coulombic efficiency is applied to negative current; SOC is not clamped unless explicitly requested.

## Data provenance
See [docs/DATA_SOURCES.md](docs/DATA_SOURCES.md). Experimental datasets are not bundled and must be checked for metadata and licence before use.

## Deferred functionality
No validated OCV-SOC curve, ECM parameters (R0/R1/C1), thermal parameters, SOH model, balancing, fault detection or safety logic is included. Do not treat unit-test success as physical validation.

## Roadmap
1. Inspect and licence-review available characterisation datasets.
2. Build reproducible OCV-SOC and pulse-test parameter-identification pipelines.
3. Add a first-order Thevenin ECM only after fitting and held-out validation.
4. Add a thermal model only after traceable thermal parameterisation and experimental comparison.
5. Extend diagnostics, pack constraints and deployment validation.

## Reference MATLAB project
[Advanced Battery Management System for Electric or Hybrid Vehicles](https://github.com/Vishal-ak/Advanced-Battery-Management-System-for-Electric-or-Hybrid-Vehicles)
