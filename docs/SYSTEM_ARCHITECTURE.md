# System Architecture

- `app.py`: Streamlit dashboard entry point.
- `src/bms/cell_library.py`: Manufacturer datasheet specifications with `None` for undocumented fields.
- `src/bms/pack_design.py`: Series/parallel pack sizing calculations.
- `src/bms/load_profiles.py`: Current profile generators, CSV validation, and numerical integration metrics.
- `src/bms/soc_estimator.py`: Trapezoidal coulomb-counting SOC estimator.
- `tests/`: Automated Pytest unit tests.
