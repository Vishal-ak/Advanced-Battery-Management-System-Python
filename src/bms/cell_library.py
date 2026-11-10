"""Manufacturer-reported cell specifications. Unknown values remain None."""

CELL_LIBRARY = {
    "Panasonic NCR18650B": {
        "manufacturer": "Panasonic/Sanyo",
        "capacity_ah_typ": 3.35,
        "capacity_ah_min": 3.25,
        "nominal_voltage_v": 3.6,
        "charge_voltage_v": 4.2,
        "discharge_cutoff_v": None,
        "standard_charge_current_a": 1.625,
        "max_charge_current_a": None,
        "max_discharge_current_a": None,
        "mass_g_max": 48.5,
        "charge_temp_c": "0 to 45",
        "discharge_temp_c": "-20 to 60",
        "source": "https://e2e.ti.com/cfs-file/__key/communityserver-discussions-components-files/196/Panasonic-NCR18650B-datasheet.pdf",
        "source_note": "Panasonic/Sanyo datasheet, version 13.11 R1 (2012)."
    },
    "LG INR18650 MJ1": {
        "manufacturer": "LG Chem",
        "capacity_ah_typ": 3.5,
        "capacity_ah_min": 3.4,
        "nominal_voltage_v": 3.635,
        "charge_voltage_v": 4.2,
        "discharge_cutoff_v": 2.5,
        "standard_charge_current_a": 1.7,
        "max_charge_current_a": 3.4,
        "max_discharge_current_a": 10.0,
        "mass_g_max": 49.0,
        "charge_temp_c": None,
        "discharge_temp_c": None,
        "source": "https://files.batteryjunction.com/frontend/files/lg/datasheet/LG-MJ1-Datasheet.pdf",
        "source_note": "LG Chem specification Rev.1 (2014-08-22), distributor-hosted copy; verify document rights before redistribution."
    },
    "Molicel INR-18650-P28A": {
        "manufacturer": "Molicel",
        "capacity_ah_typ": 2.8,
        "capacity_ah_min": 2.7,
        "nominal_voltage_v": 3.6,
        "charge_voltage_v": 4.2,
        "discharge_cutoff_v": 2.5,
        "standard_charge_current_a": 2.8,
        "max_charge_current_a": 8.4,
        "max_discharge_current_a": 35.0,
        "mass_g_max": 46.0,
        "charge_temp_c": None,
        "discharge_temp_c": None,
        "source": "https://www.molicel.com/wp-content/uploads/INR18650P28A_1.3_Product-Data-Sheet-of-INR-18650-P28A-80093.pdf",
        "source_note": "Official Molicel product datasheet."
    }
}
