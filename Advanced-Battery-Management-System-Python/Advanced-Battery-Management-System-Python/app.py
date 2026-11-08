from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent / "src"))

import streamlit as st
import pandas as pd
import plotly.express as px

from bms.cell_library import CELL_LIBRARY
from bms.pack_design import design_pack
from bms.load_profiles import (
    constant_profile, step_profile, pulse_profile, profile_metrics, validate_profile
)
from bms.soc_estimator import coulomb_count_soc

st.set_page_config(page_title="Advanced BMS | Engineering Workbench", page_icon="🔋", layout="wide")
st.title("🔋 Advanced Battery Management System")
st.caption("Python engineering workbench • pack sizing • load-profile accounting • coulomb-counting SOC • transparent data provenance")
st.warning("This is a first-order sizing and profile-analysis tool, not a validated BMS, electrochemical ECM, thermal model, or safety controller.")

page = st.sidebar.radio(
    "Workspace",
    ["Overview", "Pack Designer", "Load Profile Lab", "SOC Analysis", "Cell Library", "Data & Model Integrity"]
)

if page == "Overview":
    st.subheader("Project scope")
    a, b, c = st.columns(3)
    a.metric("Cell models", len(CELL_LIBRARY))
    b.metric("Simulation class", "Electrical accounting")
    c.metric("ECM / thermal fit", "Not included")
    st.markdown("""
    **What this version does**
    - Computes nominal pack voltage, capacity, energy, cell count, and a cell-only mass estimate when documented.
    - Builds constant, step, and pulse current profiles, or imports a CSV profile (`time_s`, `current_a`).
    - Integrates current over time for net charge transfer, nominal energy throughput, and coulomb-counting SOC.

    **What it deliberately does not claim**
    - No OCV-SOC lookup, parameter-fitted Thevenin ECM, cell balancing, SOH estimator, thermal dynamics, fault detection, or protection logic.
    - No prediction of terminal voltage, temperature rise, runtime under voltage cut-off, or safe current limits.
    """)
    st.info("Start with Pack Designer, then inspect a current profile in Load Profile Lab or SOC Analysis.")

elif page == "Pack Designer":
    st.subheader("Series/parallel pack sizing")
    cell_name = st.selectbox("Cell", list(CELL_LIBRARY))
    cell = CELL_LIBRARY[cell_name]
    left, right = st.columns(2)
    with left:
        ns = st.number_input("Series cells (Ns)", min_value=1, max_value=500, value=96, step=1)
    with right:
        np_ = st.number_input("Parallel cells (Np)", min_value=1, max_value=200, value=4, step=1)
    result = design_pack(cell, int(ns), int(np_))
    metrics = [
        ("Total cells", f"{result.total_cells:,}"),
        ("Nominal pack voltage", f"{result.nominal_voltage_v:.2f} V"),
        ("Pack capacity", f"{result.capacity_ah:.2f} Ah"),
        ("Nominal energy", f"{result.nominal_energy_kwh:.3f} kWh"),
    ]
    cols = st.columns(4)
    for col, (label, value) in zip(cols, metrics):
        col.metric(label, value)
    st.write({
        "Maximum charge voltage (series sum)": result.maximum_voltage_v,
        "Discharge cut-off voltage (series sum)": result.cutoff_voltage_v,
        "Estimated cell mass only (kg)": result.total_mass_kg,
    })
    st.caption("Pack-level values assume identical cells, ideal series/parallel grouping and no wiring, enclosure, BMS or thermal-system mass. Cell mass is not pack mass.")
    st.download_button("Download pack summary CSV", pd.DataFrame([result.__dict__]).to_csv(index=False), "pack_summary.csv", "text/csv")

elif page in ("Load Profile Lab", "SOC Analysis"):
    st.subheader("Current profile analysis" if page == "Load Profile Lab" else "Coulomb-counting SOC analysis")
    mode = st.radio("Profile source", ["Constant", "Step", "Pulse", "Upload CSV"], horizontal=True)
    dt = st.number_input("Sample interval (s)", min_value=0.1, value=1.0, step=0.1)
    if mode == "Constant":
        current = st.number_input("Current (A; + discharge / - charge)", value=5.0)
        duration = st.number_input("Duration (s)", min_value=1.0, value=3600.0)
        frame = constant_profile(current, duration, dt)
    elif mode == "Step":
        low = st.number_input("Initial current (A)", value=2.0)
        high = st.number_input("Post-step current (A)", value=10.0)
        duration = st.number_input("Duration (s)", min_value=1.0, value=1800.0)
        at = st.number_input("Step time (s)", min_value=0.0, max_value=float(duration), value=min(300.0, float(duration)))
        frame = step_profile(low, high, at, duration, dt)
    elif mode == "Pulse":
        peak = st.number_input("Pulse current (A)", value=15.0)
        pulse = st.number_input("Pulse duration (s)", min_value=0.1, value=10.0)
        rest = st.number_input("Rest duration (s)", min_value=0.0, value=20.0)
        cycles = st.number_input("Cycles", min_value=1, value=5, step=1)
        frame = pulse_profile(peak, pulse, rest, int(cycles), dt)
    else:
        uploaded = st.file_uploader("CSV with time_s and current_a columns", type=["csv"])
        if uploaded is None:
            st.info("Upload a CSV to continue.")
            st.stop()
        frame = validate_profile(pd.read_csv(uploaded))

    cell_name = st.selectbox("Cell for pack capacity reference", list(CELL_LIBRARY), key="profile_cell")
    ns = st.number_input("Series count", min_value=1, value=96, key="profile_ns")
    np_ = st.number_input("Parallel count", min_value=1, value=4, key="profile_np")
    pack = design_pack(CELL_LIBRARY[cell_name], int(ns), int(np_))

    if page == "Load Profile Lab":
        metrics = profile_metrics(frame, pack.capacity_ah, pack.nominal_voltage_v)
        fig = px.line(frame, x="time_s", y="current_a", labels={"time_s": "Time (s)", "current_a": "Current (A)"}, title="Pack current profile")
        st.plotly_chart(fig, use_container_width=True)
        cols = st.columns(4)
        for col, (key, label, fmt) in zip(cols, [
            ("net_discharge_ah", "Net discharge (Ah)", "{:.4f}"),
            ("net_soc_change_percent", "Approx. SOC change (%)", "{:.3f}"),
            ("peak_c_rate", "Peak C-rate", "{:.3f}"),
            ("nominal_energy_throughput_wh", "Nominal energy throughput (Wh)", "{:.2f}"),
        ]):
            col.metric(label, fmt.format(metrics[key]))
        st.caption("Positive current is discharge. Energy throughput uses nominal pack voltage, not instantaneous terminal voltage.")
        st.download_button("Download analysed profile CSV", frame.to_csv(index=False), "current_profile.csv", "text/csv")
    else:
        c1, c2 = st.columns(2)
        with c1:
            init_soc = st.number_input("Initial SOC (%)", min_value=0.0, max_value=100.0, value=80.0, step=1.0)
        with c2:
            eff = st.number_input("Charging coulombic efficiency", min_value=0.5, max_value=1.0, value=1.0, step=0.01)
        soc_df = coulomb_count_soc(frame, pack.capacity_ah, init_soc, eff)
        fig = px.line(soc_df, x="time_s", y="soc_percent", labels={"time_s": "Time (s)", "soc_percent": "SOC (%)"}, title="Coulomb-counting SOC vs Time")
        st.plotly_chart(fig, use_container_width=True)
        st.metric("Final SOC (%)", f"{soc_df['soc_percent'].iloc[-1]:.3f}%")
        st.caption("Limitations: Coulomb counting accumulates current-sensor bias, ignores capacity fade/temperature effects, and depends on accurate initial SOC.")
        st.download_button("Download SOC profile CSV", soc_df.to_csv(index=False), "soc_profile.csv", "text/csv")

elif page == "Cell Library":
    st.subheader("Manufacturer specification catalogue")
    for name, data in CELL_LIBRARY.items():
        with st.expander(name, expanded=(name == "Panasonic NCR18650B")):
            st.json(data)
            st.markdown(f"[Open source document]({data['source']})")
    st.caption("Values are transcribed from cited documents. A missing value is intentionally left unknown; it is not inferred from another cell.")

else:
    st.subheader("Data provenance and engineering boundaries")
    st.markdown("""
    ### Data provenance
    - Panasonic NCR18650B: Panasonic/Sanyo datasheet, version 13.11 R1 (2012), linked in the Cell Library.
    - LG INR18650 MJ1: LG Chem Rev.1 (2014-08-22), via a distributor-hosted copy. Treat as a reference; confirm document rights and revision before formal use.
    - Molicel INR-18650-P28A: official Molicel product datasheet.

    ### Model scope
    Pack arithmetic assumes identical cells and ideal interconnections. No derating, mismatch, busbar resistance, contact resistance, fuse, enclosure or cooling-system model is included.

    ### Validation status
    Unit tests cover arithmetic, input validation, profile integration, and coulomb counting. They do not validate a physical battery model.
    """)
    st.markdown("[Panasonic NCR18650B characterization dataset (Zenodo)](https://zenodo.org/records/8369275)")

st.sidebar.divider()
st.sidebar.caption("Version 1.0 • Engineering estimates only • Not for safety-critical control")
