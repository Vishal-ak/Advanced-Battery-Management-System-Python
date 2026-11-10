# Validation plan

1. Run `pytest -q`; all unit tests must pass.
2. Cross-check pack arithmetic independently: `Vpack = Ns × Vcell`, `Ahpack = Np × Ahcell`, `Whnom = Vpack × Ahpack`.
3. For profile accounting, compare constant-current integration against `I × duration / 3600` and check charging/discharging sign.
4. Before adding an ECM or thermal model, acquire cell-specific OCV-SOC, pulse/EIS, and thermal data, identify parameters on training data, and validate on held-out profiles.
