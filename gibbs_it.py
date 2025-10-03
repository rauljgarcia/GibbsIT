import math
class GibbsIT:
    '''
    ∆G = RTln(C2/C1)+ZF∆psi
    '''
    def __init__(self, name, ion, c1, c2, z, delta_psi, T=310):
        self.name = name
        self.ion = ion 
        self.c1 = c1
        self.c2 = c2
        self.z = z
        self.delta_psi = delta_psi
        self.T = T 
    
    R = 8.314e-3   # kJ/mol·K
    F = 96.5       # kJ/V·mol

    def __repr__(self):
        delta_g = self.calculate_delta_G()
        return (f"Gibbs Ion Transport({self.name}: {self.ion}, "
                f"∆G = {delta_g:.2f} kJ/mol)")

    def __eq__(self, value):
        pass

    def __lt__(self, other):
        pass

    def __add__(self, other):
        pass

    def calculate_delta_G(self):
        return (GibbsIT.R * self.T * math.log(self.c2/self.c1) + self.z 
                * self.F*self.delta_psi)


def main():
    pass
if __name__ == "__main__":
    main()