import math, functools
from typing import Union


@functools.total_ordering
class GibbsIT:
    """
    ∆G = RTln(C2/C1)+zFVm (Vm = membrane potential)
    This class models the Gibbs free energy change (∆G) for a single ion
    transport event across a biological membrane.

    inputs to __init__ are M,V,K; factory accepts mM, mV, and T as float(K) or strings
    like "37C"/"310K".
    """

    R = 8.314e-3  # Gas constant, kJ/mol K
    F = 96.5  # Faraday constant, kJ/V mol

    def __init__(
        self,
        *,
        name: str,
        ion: str,
        c_origin_M: float,
        c_dest_M: float,
        z: int,
        Vm: float,
        T_K: float = 310.0,
    ) -> None:
        self.name = name  # name of ion/transport type
        self.ion = ion  # type of ion being transferred
        self.c1 = c_origin_M  # ion concentration at origin (M)
        self.c2 = c_dest_M  # ion concentration at destination (M)
        self.z = z  # ion charge
        self.Vm = Vm  # membrane potential (V)
        self.T = T_K  # temperature (K)
        self._validate()

    def _validate(self) -> None:
        if self.c1 <= 0 or self.c2 <= 0:
            raise ValueError("Concentrations must be > 0 (M).")
        if not (-0.3 <= self.Vm <= 0.3):  # ±300 mV sanity
            raise ValueError("Vm seems not in volts (expected ±0.3 V range).")
        if self.T <= 0:
            raise ValueError("Temperature must be in Kelvin (> 0).")

    @classmethod
    def from_mM_mV(
        cls,
        *,
        name: str,
        ion: str,
        c_origin_mM: float,
        c_dest_mM: float,
        z: int,
        vm_mV: float,
        T: Union[float, str] = 310,
    ) -> "GibbsIT":
        # Temperature parsing
        if isinstance(T, str):
            t = T.strip().upper()
            if t.endswith("C"):
                T_K = float(t[:-1]) + 273.15
            elif t.endswith("K"):
                T_K = float(t[:-1])
            else:
                raise ValueError("Temperature must end with 'C' or 'K'")
        else:
            T_K = float(T)

        return cls(
            name=name,
            ion=ion,
            z=z,
            c_origin_M=c_origin_mM / 1000.0,
            c_dest_M=c_dest_mM / 1000.0,
            Vm=vm_mV / 1000.0,
            T_K=T_K,
        )

    def __repr__(self) -> str:
        dg = self.calculate_delta_G()
        return f"Gibbs Ion Transport ({self.name}: {self.ion}, ∆G = {dg:.2f} kJ/mol)"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, GibbsIT):
            return NotImplemented
        return math.isclose(
            self.calculate_delta_G(),
            other.calculate_delta_G(),
            rel_tol=1e-9,
            abs_tol=1e-9,
        )

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, GibbsIT):
            return NotImplemented
        return self.calculate_delta_G() < other.calculate_delta_G()

    def __add__(self, other: "GibbsIT") -> float:
        if not isinstance(other, GibbsIT):
            return NotImplemented
        return self.calculate_delta_G() + other.calculate_delta_G()

    def __radd__(self, other: float) -> float:
        if isinstance(other, (int, float)):
            return float(other) + self.calculate_delta_G()
        return NotImplemented

    def calculate_delta_G(self) -> float:
        return (
            GibbsIT.R * self.T * math.log(self.c2 / self.c1) + self.z * self.F * self.Vm
        )
