# Gibbs Ion Transport (GibbsIT)

**GibbsIT** is a Python class that models the Gibbs free energy change (ΔG) for ion transport across biological membranes.  
It implements the thermodynamic relationship:

$$
\Delta G = RT \ln\left(\frac{C_2}{C_1}\right) + zF\Delta\psi
$$

GibbsIT began as an object-oriented Python exercise and has since evolved into a portfolio project focused on scientific software development. It demonstrates thermodynamic modeling, unit conversion, input validation, and automated testing with pytest.

The class provides unit-safe calculations and input validation for analyzing the energetic favorability of ion transport events.


## Features

- Calculates Gibbs free energy (ΔG) for ion transport across biological membranes
- Accepts either the class's standard calculation units **(M, V, K)** or common biological units **(mM, mV, °C)** via an alternate constructor  
- Built-in validation checks for realistic physiological values  
- Designed for readability and educational use  
- Easily extended for batch analyses or plotting

## Example Usage

```python
from gibbs_it import GibbsIT

# Using the class's standard calculation units
na_in = GibbsIT(
    name="Na influx",
    ion="Na+",
    c_origin_M=0.145,
    c_dest_M=0.015,
    z=1,
    Vm=-0.07,
    T_K=310.15
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
    vm_mV=-70,
    T="37C"
)
print(ca_in)
# Gibbs Ion Transport (Ca influx: Ca2+, ∆G = -38.76 kJ/mol)
```

## Testing

The project includes a pytest test suite covering:

- Gibbs free energy (ΔG) calculations
- Alternate constructor unit conversions
- Input validation
- Boundary-condition testing

Run the test suite from the project directory with:

```bash
python -m pytest -v
```

## Installation

Clone the repository:
```bash 
git clone https://github.com/rauljgarcia/GibbsIT.git
cd GibbsIT
```
Run the examples or execute the test suite from the project directory.

The GibbsIT package requires only the Python standard library. Running the test suite additionally requires pytest.

## Scientific Background

This project is based on classical thermodynamics applied to biological ion transport.
The equation includes contributions from:
- Concentration gradient (RT ln(C₂/C₁))
- Membrane potential (zFΔψ)

Such calculations are useful for understanding energy requirements in systems like:
- Na⁺/K⁺-ATPase pumps
- Ca²⁺ transport in muscle contraction
- Neuronal membrane potential dynamics


## Future Enhancements
- Support batch calculations from CSV files
- Generate plots of ΔG versus membrane potential or concentration ratio
- Build a simple command-line interface
- Develop a graphical interface for educational use


## Author

Raul Garcia

Bioinformatics graduate interested in computational biology,
biochemistry, genomics, and scientific software development.

[GitHub Profile](https://github.com/rauljgarcia)
