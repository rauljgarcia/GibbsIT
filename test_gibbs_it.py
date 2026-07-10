from gibbs_it import GibbsIT
import pytest

def test_delta_g_for_na_influx():
    """Verify the ΔG calculation for a representative sodium influx example."""
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

def test_from_mM_mV_for_conversion():
    """Verify that the alternate constructor converts biological input units to the class's internal units."""
    na = GibbsIT.from_mM_mV(
        name="Na influx",
        ion="Na+",
        c_origin_mM=145,
        c_dest_mM=15,
        z=1,
        vm_mV=-70,
        T="37C",
    )
    expected_origin = 0.145
    expected_dest = 0.015
    expected_vm = -0.070
    expected_T = 310.15

    assert na.c1 == pytest.approx(expected_origin)
    assert na.c2 == pytest.approx(expected_dest)
    assert na.Vm == pytest.approx(expected_vm)
    assert na.T == pytest.approx(expected_T)

def test_origin_concentration_must_be_positive():
    """Verify that a non-positive value for origin ion concentration is rejected."""
    with pytest.raises(ValueError):
        GibbsIT(
            name="Invalid c",
            ion="Na+",
            c_origin_M=-0.001,
            c_dest_M=0.015,
            z=1,
            Vm=-70
        )

def test_vm_outside_sanity_range_raises_error():
    """Verify that unrealistically large positive membrane potential is rejected."""
    with pytest.raises(ValueError):
        GibbsIT(
            name="Invalid Vm",
            ion="Na+",
            c_origin_M=0.145,
            c_dest_M=0.015,
            z=1,
            Vm=0.500
            )
        