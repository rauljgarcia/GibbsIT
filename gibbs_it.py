"""
gibbs_it.py

A lightweight Python module for calculating Gibbs free energy change (ΔG)
for ion transport across biological membranes.

This module provides:
    - GibbsIT class with unit conversion and input validation
    - Operator overloading for comparison and addition
    - A convenient factory method for non-SI units

Example:
    >>> from gibbs_it import GibbsIT
    >>> na = GibbsIT.from_mM_mV(
    ...     name="Na influx",
    ...     ion="Na+",
    ...     c_origin_mM=145,
    ...     c_dest_mM=15,
    ...     z=1,
    ...     vm_mV=-70,
    ...     T="37C",
    ... )
    >>> print(na)
    Gibbs Ion Transport (Na influx: Na+, ∆G = -12.60 kJ/mol)
"""

import math, functools
from typing import Union


@functools.total_ordering
class GibbsIT:
    """
    Calculate Gibbs free energy change (ΔG) for ion transport across a biological membrane.

    The calculation is based on the equation:
        ΔG = R * T * ln(C2 / C1) + z * F * Vm

    where:
        R  - gas constant (8.314e-3 kJ/mol·K)
        T  - absolute temperature (K)
        C1 - ion concentration at origin (M)
        C2 - ion concentration at destination (M)
        z  - ion charge
        F  - Faraday constant (96.5 kJ/V·mol)
        Vm - membrane potential (V)

    Inputs to `__init__` are expected in SI units (M, V, K).
    Use the `from_mM_mV` classmethod for more convenient inputs (mM, mV, °C/K as strings or floats).
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
        """
        Initialize a GibbsIT object with SI units.

        Parameters:
            name (str): Descriptive name of the transport process.
            ion (str): Ion being transported (e.g., 'Na+').
            c_origin_M (float): Origin concentration in molar (M).
            c_dest_M (float): Destination concentration in molar (M).
            z (int): Ion charge (e.g., +1 for Na+, +2 for Ca²⁺).
            Vm (float): Membrane potential in volts (V).
            T_K (float, optional): Temperature in Kelvin (default is 310 K).
        """
        self.name = name  # name of ion/transport type
        self.ion = ion  # type of ion being transferred
        self.c1 = c_origin_M  # ion concentration at origin (M)
        self.c2 = c_dest_M  # ion concentration at destination (M)
        self.z = z  # ion charge
        self.Vm = Vm  # membrane potential (V)
        self.T = T_K  # temperature (K)
        self._validate()

    def _validate(self) -> None:
        """
        Validate input values to ensure they are within reasonable physical ranges.

        Raises:
            ValueError: If concentrations are <= 0, Vm is outside ±0.3 V,
                        or temperature is not positive.
        """
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
        """
        Alternate constructor using non-SI units (mM, mV, and °C/K).

        Parameters:
            name (str): Descriptive name of the transport process.
            ion (str): Ion being transported (e.g., 'Na+').
            c_origin_mM (float): Origin concentration in millimolar (mM).
            c_dest_mM (float): Destination concentration in millimolar (mM).
            z (int): Ion charge.
            vm_mV (float): Membrane potential in millivolts (mV).
            T (float or str, optional): Temperature in Kelvin (float) or as a string
                                        (e.g., '37C', '310K'). Default is 310 K.

        Returns:
            GibbsIT: Instance of GibbsIT with converted SI units.
        """
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
        """
        Return a readable string representation of the GibbsIT object.

        Returns:
            str: A string showing the name, ion, and ΔG value in kJ/mol.
        """
        dg = self.calculate_delta_G()
        return f"Gibbs Ion Transport ({self.name}: {self.ion}, ∆G = {dg:.2f} kJ/mol)"

    def __eq__(self, other: object) -> bool:
        """
        Compare two GibbsIT instances for equality based on ΔG.

        Parameters:
            other (object): Another GibbsIT instance.

        Returns:
            bool: True if ΔG values are equal within tolerance, False otherwise.
        """
        if not isinstance(other, GibbsIT):
            return NotImplemented
        return math.isclose(
            self.calculate_delta_G(),
            other.calculate_delta_G(),
            rel_tol=1e-9,
            abs_tol=1e-9,
        )

    def __lt__(self, other: object) -> bool:
        """
        Compare ΔG values of two GibbsIT instances.

        Parameters:
            other (object): Another GibbsIT instance.

        Returns:
            bool: True if this ΔG is less than the other's, False otherwise.
        """
        if not isinstance(other, GibbsIT):
            return NotImplemented
        return self.calculate_delta_G() < other.calculate_delta_G()

    def __add__(self, other: "GibbsIT") -> float:
        """
        Add ΔG values of two GibbsIT instances.

        Parameters:
            other (GibbsIT): Another GibbsIT instance.

        Returns:
            float: Sum of ΔG values (kJ/mol).
        """
        if not isinstance(other, GibbsIT):
            return NotImplemented
        return self.calculate_delta_G() + other.calculate_delta_G()

    def __radd__(self, other: float) -> float:
        """
        Allow summing GibbsIT instances with numbers (e.g., sum([a, b], 0.0)).

        Parameters:
            other (float): A numeric value to add.

        Returns:
            float: Sum of ΔG and the number.
        """
        if isinstance(other, (int, float)):
            return float(other) + self.calculate_delta_G()
        return NotImplemented

    def calculate_delta_G(self) -> float:
        """
        Calculate Gibbs free energy change (ΔG) in kJ/mol.

        Returns:
            float: The ΔG value in kJ/mol.
        """
        return (
            GibbsIT.R * self.T * math.log(self.c2 / self.c1) + self.z * self.F * self.Vm
        )
