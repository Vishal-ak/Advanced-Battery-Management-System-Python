import pytest
from bms.load_profiles import constant_profile
from bms.soc_estimator import coulomb_count_soc

def test_coulomb_count_discharge():
    f = constant_profile(2.0, 3600.0, 60.0)
    df = coulomb_count_soc(f, pack_capacity_ah=4.0, initial_soc_percent=80.0)
    assert df["soc_percent"].iloc[-1] == pytest.approx(30.0)

def test_coulomb_count_charge_with_efficiency():
    f = constant_profile(-2.0, 3600.0, 60.0)
    df = coulomb_count_soc(f, pack_capacity_ah=4.0, initial_soc_percent=20.0, coulombic_efficiency=0.9)
    assert df["soc_percent"].iloc[-1] == pytest.approx(65.0)
