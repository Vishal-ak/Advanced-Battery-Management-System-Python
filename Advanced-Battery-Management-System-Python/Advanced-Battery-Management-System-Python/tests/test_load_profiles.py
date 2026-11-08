import pytest
import pandas as pd
from bms.load_profiles import constant_profile, step_profile, pulse_profile, profile_metrics, validate_profile

def test_constant_profile_net_ah():
    f = constant_profile(3, 3600, 60)
    m = profile_metrics(f, 3, 3.6)
    assert m["net_discharge_ah"] == pytest.approx(3.0)
    assert m["net_soc_change_percent"] == pytest.approx(-100.0)

def test_step_profile_values():
    f = step_profile(1, 5, 2, 4, 1)
    assert f.current_a.tolist() == [1.0, 1.0, 5.0, 5.0, 5.0]

def test_pulse_profile_has_rest():
    f = pulse_profile(10, 2, 2, cycles=2, dt_s=1)
    assert 0.0 in f.current_a.values
    assert 10.0 in f.current_a.values

def test_non_monotonic_time_rejected():
    with pytest.raises(ValueError):
        validate_profile(pd.DataFrame({"time_s": [0, 1, 1], "current_a": [1, 2, 3]}))

def test_charge_sign_convention():
    f = constant_profile(-2, 3600, 60)
    m = profile_metrics(f, 4, 3.6)
    assert m["net_discharge_ah"] == pytest.approx(-2.0)
    assert m["peak_charge_current_a"] == pytest.approx(2.0)
