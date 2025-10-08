Gibbs Ion Transport (GibbsIT)

GibbsIT is a Python class that models the Gibbs free energy change (ΔG) for ion transport across biological membranes.
It implements the thermodynamic relationship:

\Delta G = RT \ln\left(\frac{C_2}{C_1}\right) + zF\Delta\psi

The class provides unit-safe calculations and Pythonic comparison tools for analyzing the energetic favorability of ion movements such as Na⁺ influx or Ca²⁺ efflux in biological systems.

⸻

🔍 Features
	•	Calculates ΔG for ion transport events using the Nernst equation form
	•	Accepts either SI units (M, V, K) or lab-friendly units (mM, mV, °C) via an alternate constructor
	•	Built-in validation checks for realistic physiological values
	•	Operator overloading:
	•	__lt__ → Compare ΔG values (<, >)
	•	__eq__ → Check energetic equivalence
	•	__add__ → Combine ΔG values for multiple ion events
	•	Designed for readability and educational use
	•	Easily extended for batch analyses or plotting

⸻

Example Usage
from gibbs_it import GibbsIT

# Using SI units directly
na_in = GibbsIT(
    name="Na influx",
    ion="Na+",
    c_origin_M=0.145,
    c_dest_M=0.015,
    z=1,
    delta_psi_V=-0.07,
    T_K=310
)
print(na_in)
# Gibbs Ion Transport (Na influx: Na+, ∆G = -12.60 kJ/mol)

# Using alternate constructor for mM/mV and °C input
ca_in = GibbsIT.from_mM_mV(
    name="Ca influx",
    ion="Ca2+",
    c_origin_mM=1.8,
    c_dest_mM=0.0001,
    z=2,
    delta_psi_mV=-70,
    T="37C"
)
print(ca_in)
# Gibbs Ion Transport (Ca influx: Ca2+, ∆G = -38.76 kJ/mol)

# Compare and add
if ca_in < na_in:
    print("Ca influx is more energetically favorable")
net_energy = ca_in + na_in
print(f"Combined ΔG = {net_energy:.2f} kJ/mol")

Installation
git clone https://github.com/rauljgarcia/GibbsIT.git
cd GibbsIT

No external dependencies are required beyond the Python standard library.

Scientific Background

This project is based on classical thermodynamics applied to biological ion transport.
The formula used accounts for both:
	•	Concentration gradient (RT ln(C₂/C₁))
	•	Membrane potential (zFΔψ)

Such calculations are essential for understanding energy requirements in systems like:
	•	Na⁺/K⁺-ATPase pumps
	•	Ca²⁺ transport in muscle contraction
	•	Neuronal membrane potential dynamics

⸻

🚀 Future Enhancements
	•	Add support for batch calculations using lists or Pandas DataFrames
	•	Include a plotting module to visualize ΔG vs. ion gradient
	•	Implement a command-line interface (CLI)
	•	Add unit tests with pytest
	•	Optional integration with Jupyter notebooks for teaching demos

⸻

Author

Raul Garcia
Bioinformatics student at the University of Arizona
Exploring the intersection of programming, biochemistry, and computational modeling.

🔗 GitHub Profile
