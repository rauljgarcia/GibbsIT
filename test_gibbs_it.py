from gibbs_it import GibbsIT
import pytest

def test_delta_g_for_na_influx():
    na = GibbsIT.from_mM_mV(
        name="Na influx",
        ion="Na+",
        c_origin_mM=145,
        c_dest_mM=15,
        z=1,
        vm_mV=-70,
        T="37C",
    )
    expected = -12.6
    assert na.calculate_delta_G() == pytest.approx(expected, abs=0.1)
