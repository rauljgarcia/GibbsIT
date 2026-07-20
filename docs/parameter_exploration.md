# Parameter exploration
This phase calculates ΔG using the GibbsIT calculator, based on the Gibbs ion transfer equation:

$$
\Delta G = RT \ln\left(\frac{C_2}{C_1}\right) + zF\Delta\psi
$$

## Inputs
This package will use three types of inputs:
1. Universal constants, fixed and hard-coded, hidden from the user. 
- R
- F


2. Ion identity
The user chooses the ions, which automatically determine z internally. The available options 
are initially limited to:

- Na⁺
- K⁺
- Ca²⁺
- Mg²⁺
- Cl⁻

3. Physiological State
The user defines the biological system using the following physiological variables:
- Temperature 
- Intracellular ion concentration
- Extracellular ion concentration
- Membrane Potential
The quantities are manipulated by the user and define a particular physiological scenario.

## Central goal and workflow
The user defines a baseline physiological state and selects one physiological variable to vary across a specified range. GibbsIT holds all remaining inputs constant, calculates ΔG at each value, returns the resulting dataset, and plots ΔG as a function of the selected variable.

For example:

Baseline:
- Ion = Na⁺
- Temperature = 310.15 K
- C<sub>in</sub> = 15 mM
- C<sub>out</sub> = 145 mM
- Membrane potential = -70 mV

Variable explored:

Membrane potential = -100 to +40 mV

The output would be a series of ΔG values and a plot of ΔG values versus membrane potential.

Parameter exploration does not implement the Gibbs equation itself. Instead it repeatedly invokes the GibbsIT calculator, while varying a single physiological variable. This ensures that the Gibbs equation is implemented in one place and reused consistently throughout the package.

This phase is limited to varying a single physiological variable while holding all others constant. Support for varying multiple parameters simultaneously or importing experimental datasets may be considered in future versions.


