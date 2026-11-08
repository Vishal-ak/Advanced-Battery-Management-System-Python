# Advanced Battery Management System — Python

A reproducible Python engineering workbench for lithium-ion pack sizing, current-profile accounting, and coulomb-counting SOC analysis.

> **Engineering boundary:** this release is not a validated BMS or safety controller. It intentionally excludes ECM voltage prediction, thermal prediction, and SOH estimation because no cell-specific fitted/validated parameter set is included.

## Run locally
```bash
git clone https://github.com/Vishal-ak/Advanced-Battery-Management-System-Python.git
cd Advanced-Battery-Management-System-Python
python -m venv .venv
pip install -r requirements.txt
streamlit run app.py
```

## Run tests
```bash
pytest -q
```
