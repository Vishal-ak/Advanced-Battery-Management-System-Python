import pytest
from bms.cell_library import CELL_LIBRARY
from bms.pack_design import design_pack

def test_panasonic_pack_arithmetic():
    r = design_pack(CELL_LIBRARY["Panasonic NCR18650B"], 10, 3)
    assert r.total_cells == 30
    assert r.nominal_voltage_v == pytest.approx(36.0)
    assert r.maximum_voltage_v == pytest.approx(42.0)
    assert r.capacity_ah == pytest.approx(10.05)
    assert r.nominal_energy_wh == pytest.approx(361.8)

def test_unknown_cutoff_is_not_invented():
    r = design_pack(CELL_LIBRARY["Panasonic NCR18650B"], 4, 2)
    assert r.cutoff_voltage_v is None

@pytest.mark.parametrize("s,p", [(0, 1), (1, 0), (-1, 2)])
def test_rejects_invalid_counts(s, p):
    with pytest.raises(ValueError):
        design_pack(CELL_LIBRARY["Panasonic NCR18650B"], s, p)

def test_rejects_non_integer_counts():
    with pytest.raises(TypeError):
        design_pack(CELL_LIBRARY["Panasonic NCR18650B"], 2.5, 3)
