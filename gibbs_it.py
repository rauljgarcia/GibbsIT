import math, functools

@functools.total_ordering
class GibbsIT:
    '''
    ∆G = RTln(C2/C1)+zF∆psi
    This class models the Gibbs free energy change (∆G) for a single ion 
    transport event across a biological membrane.
    '''
    def __init__(self, name, ion, c1, c2, z, delta_psi, T = 310):
        self.name = name # name of ion/transport type
        self.ion = ion # type of ion being transferred
        self.T = T # temp in K, default to 310
        self.c1 = c1/1000 # ion concentration at origin (mM to M)
        self.c2 = c2/1000 # ion concentration at destination (mM to M)
        self.z = z # ion charge
        self.delta_psi = delta_psi/1000 # mV to V
        
    R = 8.314e-3   # Gas constant, kJ/mol K
    F = 96.5       # Faraday constant, kJ/V mol

    def __repr__(self):
        delta_g = self.calculate_delta_G()
        return (f"Gibbs Ion Transport ({self.name}: {self.ion}, "
                f"∆G = {delta_g:.2f} kJ/mol)")

    def __eq__(self, other):
        if not isinstance(other, GibbsIT):
            return NotImplemented
        return math.isclose(other.calculate_delta_G(), self.calculate_delta_G())

    def __lt__(self, other):
        if isinstance(other, GibbsIT):
            return self.calculate_delta_G() < other.calculate_delta_G()

    def __add__(self, other):
        if isinstance(other, GibbsIT):
            return self.calculate_delta_G() + other.calculate_delta_G()

    def calculate_delta_G(self):
        return (GibbsIT.R * self.T * math.log(self.c2/self.c1) 
                + self.z * self.F * self.delta_psi)


def main():
    
    # test repr
    ca_in = GibbsIT("Ca influx", "Ca2+", 1.8, 0.0001, 2, -70, 310)
    print(ca_in) # ∆G = -38.76
    na_in = GibbsIT("Na influx", "Na+", 145, 15, 1, -70, 310)
    print(na_in) # ∆G = -12.6
    
    # test lt
    if(ca_in < na_in):
        print('Ca influx more favorable')
    elif(na_in < ca_in):
        print('Na influx more favorable')
    else:
        print("Invalid comparison")

    # test eq
    na_in2 = GibbsIT("Na influx", "Na+", 145, 15, 1, -70, 310)
    print(na_in == na_in2)

    # test add
    na_out = GibbsIT("Na efflux", "Na+", 15, 145, 1, -70, 310)
    print(na_out) # ∆G = -0.91
    net_na = na_in + na_out
    print(f"Net energy {net_na:.2f} kJ/mol") # -12.6 + -0.91 = -13.51

if __name__ == "__main__":
    main()