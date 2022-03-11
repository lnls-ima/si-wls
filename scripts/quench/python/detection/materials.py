import numpy as _np
import matplotlib.pyplot as plt
import sys as _sys
import traceback as _traceback

class Copper:
    """ Class to hold copper properties 
    
        Refs.: 
        [1] M. McAshan, "MIITS Integrals for Copper and for Nb-46Ti"
        [2] KN5010 Nº4 (Davide)
        [3] https://www.copper.org/resources/properties/cryogenic/   
        [4] https://www.copper.org/resources/properties/atomic_properties.html
        [5]  Bradley, P., Radebaugh, R., "Properties of Selected Materials at Cryogenic Temperatures", NIST, 2013: https://www.nist.gov/publications/properties-selected-materials-cryogenic-temperatures
        
    """

    def __init__(self):    

        # Ref.: [4] [kg/m³]
        self.density = 8940

        # Refs.: [5] [J/Kg.K]
        self._specific_heat_data = {
            'T':
                _np.array([4.0, 6.0, 8.0, 10.0, 12.0, 14.0, 16.0, 18.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0, 120.0, 140.0, 160.0, 180.0, 200.0, 220.0, 240.0, 260.0, 280.0, 300.0]),

            'c': _np.array([0.09942, 0.2303, 0.4639, 0.8558, 1.47, 2.375, 3.64, 5.327, 7.491, 26.4, 57.63, 95.84, 135.2, 171.8, 203.8, 230.9, 253.5, 287.6, 311.6, 329.4, 343.4, 355, 364.7, 372.6, 378.6, 382.5, 384])
        }

        # Refs.: [3],[5]
        self._thermal_conductivity_per_rrr_data = {
            50: {
                'T': 
                    _np.array([4.0, 6.0, 8.0, 10.0, 12.0, 14.0, 16.0, 18.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0, 120.0, 140.0, 160.0, 180.0, 200.0, 220.0, 240.0, 260.0, 280.0, 300.0]),

                'k':
                    _np.array([320.4, 466.8, 622.3, 778.1, 927.3, 1064.0, 1185.0, 1287.0, 1368.0, 1444.0, 1163.0, 863.6, 670.0, 561.1, 500.3, 465.1, 443.9, 421.8, 411.6, 406.0, 402.6, 400.1, 398.2, 396.5, 395.0, 393.6, 392.4])
            },

            100: {
                'T': 
                    _np.array([4.0, 6.0, 8.0, 10.0, 12.0, 14.0, 16.0, 18.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0, 120.0, 140.0, 160.0, 180.0, 200.0, 220.0, 240.0, 260.0, 280.0, 300.0]),

                'k':
                    _np.array([642.3, 931.7, 1239.0, 1540.0, 1814.0, 2045.0, 2226.0, 2352.0, 2423.0, 2143.0, 1485.0, 1005.0, 741.2, 603.6, 529.3, 487.0, 461.5, 434.8, 422.1, 415.0, 410.3, 407.0, 404.2, 401.9, 399.9, 398.0, 396.3])
            },

            200: {
                'T': 
                    _np.array([3.9415, 4.0000, 4.8801, 5.3705, 6.0423, 7.0531, 8.3552, 9.3312, 10.8120, 12.0750, 14.6240, 16.5750, 18.5110, 20.0740, 30.7730, 40.7130, 50.0380, 60.1550, 70.2180, 80.1740, 90.2020, 100.0000, 120.2200, 140.3300, 161.4100, 180.2700, 201.3300, 249.2700, 299.6700]),

                'k':
                    _np.array([1284.10, 1311.10, 1631.80, 1830.00, 2073.70, 2399.30, 2747.40, 2986.20, 3279.70, 3455.10, 3678.00, 3755.40, 3716.50, 3639.90, 2580.90, 1631.80, 1075.70, 803.48, 652.35, 569.71, 518.72, 487.28, 462.55, 443.67, 430.02, 425.56, 416.78, 408.19, 408.19])
            },

            300: {
                'T': 
                    _np.array([4.0, 6.0, 8.0, 10.0, 12.0, 14.0, 16.0, 18.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0, 120.0, 140.0, 160.0, 180.0, 200.0, 220.0, 240.0, 260.0, 280.0, 300.0]),

                'k':
                    _np.array([1926.6, 2810.0, 3636.0, 4320.0, 4829.0, 5147.0, 5276.0, 5234.0, 5052.0, 3257.0, 1833.0, 1130.0, 801.8, 638.5, 551.0, 501.0, 471.1, 440.6, 427.6, 421.2, 417.5, 414.6, 411.8, 408.8, 405.5, 401.8, 397.9])
            }
        }

    def calc_resistivity(self, T, RRR, B):
    # Ref.: [1] [Ohm.m]
        return _np.multiply(
            1e-8,
            _np.add(
                _np.divide(1.545, _np.float_(RRR)),
                _np.divide(
                    1,
                    _np.add(
                        _np.add(
                            _np.divide(2.32547*1e9, _np.power(_np.float_(T), 5)),
                            _np.divide(9.57137*1e5, _np.power(_np.float_(T), 3))
                            ),
                        _np.divide(1.62735*1e2, _np.float_(T))
                        )
                    )
                )
            )

    def calc_specific_heat(self, T):
        return _np.interp(
            T,
            self._specific_heat_data['T'],
            self._specific_heat_data['c']
            )

    def calc_avg_specific_heat(self, T1, T2, num_steps=1000):
        x = _np.linspace(T1, T2, num=num_steps, endpoint=True)
        y = _np.array([self.calc_specific_heat(T) for T in x])
        integral_val = _np.trapz(y, x)
        return integral_val / (T2 - T1)

    def calc_thermal_conductivity(self, T, RRR):
        
        return _np.interp(
            T,
            self._thermal_conductivity_per_rrr_data[RRR]['T'],
            self._thermal_conductivity_per_rrr_data[RRR]['k']
            )

    def calc_avg_thermal_conductivity(self, T1, T2, RRR, num_steps=1000):
        x = _np.linspace(T1, T2, num=num_steps, endpoint=True)
        y = _np.array([self.calc_thermal_conductivity(T, RRR) for T in x])
        integral_val = _np.trapz(y, x)
        return integral_val / (T2 - T1)

    def calc_properties(self, T, RRR, B):
        
        dsty = self.density                         # [kg/m³]
        rho = self.calc_resistivity(T, RRR, B)      # [Ohm.m]
        c = self.calc_specific_heat(T)              # [J/kg.K]
        k = self.calc_thermal_conductivity(T, RRR)  # [W/m.K]

        return [dsty, rho, c, k]

    def calc_avg_properties(self, T1, T2, RRR, B):
        
        dsty = self.density                                  # [kg/m³]
        rho = self.calc_resistivity(T2, RRR, B)               # [Ohm.m]
        c = self.calc_avg_specific_heat(T1, T2)              # [J/kg.K]
        k = self.calc_avg_thermal_conductivity(T1, T2, RRR)  # [W/m.K]

        return [dsty, rho, c, k]

    def calc_magnetoresistivity(self, T, RRR, B):
        rho_0 = self.calc_resistivity(T, RRR, 0)
        S = _np.divide(
                self.calc_resistivity(273, RRR, 0),
                rho_0
            )
        log_x = _np.log10(
            _np.multiply(B, S)
        )
        log_delta_rho = _np.add(
            _np.add(
                -2.662,
                _np.add(
                    _np.multiply(0.3168, log_x),
                    _np.multiply(0.6229, _np.power(log_x, 2))
                )
            ),
            _np.add(
                _np.multiply(-0.1839, _np.power(log_x, 3)),
                _np.multiply(0.01827, _np.power(log_x, 4))
            )
        )
        return _np.power(10, log_delta_rho) * rho_0 + rho_0

class NbTi:
    """ Class to hold NbTi properties 
    
        Refs.: 
        [1] Akbar and Keller. Thermal Analysis and Simulation of the Superconducting Magnet in the SpinQuestExperiment at Fermilab.
        [2] https://onlinelibrary.wiley.com/doi/pdf/10.1002/9783527635467.app1
        [3] https://qps.web.cern.ch/download/pdf/Quench_Wilson_1.pdf
        [4] M. McAshan, "MIITS Integrals for Copper and for Nb-46Ti
        [5] Russenschuck, S., "Field Computation for Accelerator Magnets",
            Appendix A, Wiley, 2010
    """
    def __init__(self):

        # Ref.: [1-2] [kg/m³]
        self.density = 6000

        # Ref.: [3] [kg/m³]
        self.density = 6200

        # Critical temperature [K]
        self.Tc = 9.2

        # Ref.: [4] Table IV [J/Kg.K]
        self._specific_heat_data_nc = {

            'T':
                _np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340]),

            'c':
                _np.array([0.00432, 0.0246, 0.0685, 0.124, 0.176, 0.219, 0.253, 0.279, 0.300, 0.317, 0.341, 0.357, 0.369, 0.378, 0.385, 0.391, 0.396, 0.400, 0.404, 0.407, 0.410, 0.413]) * 1e3 
        }

    def calc_resistivity(self, T, is_sc):
        # Ref.: [?] [Ohm.m]
        if is_sc:
            return 1e-5
        else:
            return 1e-5

    def calc_specific_heat(self, T, B, is_sc):
        
        # Ref [4] Table IV 
        #
        # Due to good continuity between this and the last condition, this
        # function is used for normal conducting and T >= 20 K, instead of  
        # T >= 10 K. This way, a smoother transition from 10 K to 20 K is
        # obtained than from the interpolation provided in this one.
        #
        # [J/Kg.K]
        if T >= 20:
            return _np.interp(
                T,
                self._specific_heat_data_nc['T'],
                self._specific_heat_data_nc['c']
                )

        # Ref [1] Eq. 22 | Ref [5] Eq. A.25
        #
        # This formula is only used for superconducting condition and T < Tc 
        # (9.2 K).
        #
        # [J/Kg.K]
        elif is_sc and T < self.Tc:
            return _np.add(
                _np.multiply(0.0082, _np.power(_np.float_(T), 3)),
                _np.multiply(0.011, 
                    _np.multiply(_np.float_(B), _np.float_(T))
                    )
                )

        # Ref[4] Eq. Cp(T < 10 K) 
        #
        # Due to good continuity between this and the first condition, this
        # function is used for normal conducting and T < 20 K, instead of  
        # T < 10 K. This way, a smoother transition from 10 K to 20 K is
        # obtained than from the interpolation provided in the other one.
        #
        # [J/Kg.K]
        else:
            return _np.add(
                _np.multiply(0.002711, _np.power(_np.float_(T), 3)),
                _np.multiply(0.161, _np.float_(T))
                )

    def calc_avg_specific_heat(self, T1, T2, B, is_sc, num_steps=1000):
        x = _np.linspace(T1, T2, num=num_steps, endpoint=True)
        y = _np.array([self.calc_specific_heat(T, B, is_sc) for T in x])
        integral_val = _np.trapz(y, x)
        return integral_val / (T2 - T1)

    def calc_thermal_conductivity(self, T):
        # Ref[5] Eq. A.20
        # [W/m.K]
        p = [-5.0e-14, 1.5e-11, 6.0e-9, -3.0e-6, 3.0e-4, 4.56e-2, 6.6e-2]
        return _np.polyval(p,T)

    def calc_avg_thermal_conductivity(self, T1, T2, num_steps=1000):
        x = _np.linspace(T1, T2, num=num_steps, endpoint=True)
        y = _np.array([self.calc_thermal_conductivity(T) for T in x])
        integral_val = _np.trapz(y, x)
        return integral_val / (T2 - T1)

    def calc_properties(self, T, RRR, B, is_sc):
        
        dsty = self.density                         # [kg/m³]
        rho = self.calc_resistivity(T, is_sc)       # [Ohm.m]
        c = self.calc_specific_heat(T, B, is_sc)    # [J/kg.K]
        k = self.calc_thermal_conductivity(T)       # [W/m.K]

        return [dsty, rho, c, k]

    def calc_avg_properties(self, T1, T2, RRR, B, is_sc):
        
        dsty = self.density                                  # [kg/m³]
        rho = self.calc_resistivity(T2, is_sc)                # [Ohm.m]
        c = self.calc_avg_specific_heat(T1, T2, B, is_sc)    # [J/kg.K]
        k = self.calc_avg_thermal_conductivity(T1, T2)       # [W/m.K]

        return [dsty, rho, c, k]

class SCWire:
    def __init__(self, parameters: dict):
    
        [Iop, B, Top, Tc, Tcs, RRR, ratio_cu_sc, d_cond] = parameters.values()
        
        [s_sc, s_cu] = self.calc_area_sc_cu(d_cond, ratio_cu_sc)
        
        # Transition temperature [K]
        self.Tjoule = _np.divide(_np.add(Tc, Tcs), 2)

        # Is superconducting?
        is_sc = True

        copper = Copper()
        nbti = NbTi()

        [dsty_cu, resty_cu, c_cu, k_cu] = copper.calc_properties(
                                                self.Tjoule, RRR, B
                                                )
        
        [dsty_sc, resty_sc, c_sc, k_sc] = nbti.calc_properties(
                                                self.Tjoule, RRR, B, is_sc
                                                )
        [avg_dsty_cu, avg_resty_cu, avg_c_cu, avg_k_cu] = copper.calc_avg_properties(
                                                Top, self.Tjoule, RRR, B
                                                )
        
        [avg_dsty_sc, avg_resty_sc, avg_c_sc, avg_k_sc] = nbti.calc_avg_properties(
                                                Top, self.Tjoule, RRR, B, is_sc
                                                )

        # Residual resistivity ratio
        self.RRR = RRR
        
        # Cu/Nb-Ti ratio
        self.ratio_cu_sc = ratio_cu_sc

        # Total conductor diameter [mm]
        self.d_cond = d_cond
        
        # Nb-Ti, copper and total conductor area [m²]
        self.s_sc = s_sc
        self.s_cu = s_cu
        self.s_cond = _np.add(s_sc, s_cu)

        # Nb-Ti and copper area fraction 
        self.f_sc = _np.divide(s_sc, self.s_cond)
        self.f_cu = _np.divide(s_cu, self.s_cond)
        
        #   Composite density [kg/m³K]
        self.dsty_comp = _np.add(
                _np.multiply(self.f_cu, dsty_cu),
                _np.multiply(self.f_sc, dsty_sc)
                )

        #   Composite resistivity [Ohm.m]
        self.resty_comp = _np.divide(
                                _np.multiply(resty_cu, resty_sc),
                                _np.add(
                                    _np.multiply(resty_cu, self.f_sc),
                                    _np.multiply(resty_sc, self.f_cu)
                                    )
                            )
        
        #   Composite specific heat [J/kg.K]
        self.c_comp = _np.add(
                _np.multiply(self.f_cu, c_cu),
                _np.multiply(self.f_sc, c_sc)
                )

        #   Average composite specific heat [J/kg.K]
        self.avg_c_comp = _np.add(
                _np.multiply(self.f_cu, avg_c_cu),
                _np.multiply(self.f_sc, avg_c_sc)
                )
        
        #   Composite volumetric specific heat [J/m³.K]
        self.C_comp = _np.add(
                _np.multiply(_np.multiply(self.f_cu, dsty_cu), c_cu),
                _np.multiply(_np.multiply(self.f_sc, dsty_sc), c_sc)
                )


        #   Average composite volumetric specific heat [J/m³.K]
        self.avg_C_comp = _np.add(
                _np.multiply(_np.multiply(self.f_cu, dsty_cu), avg_c_cu),
                _np.multiply(_np.multiply(self.f_sc, dsty_sc), avg_c_sc)
                )
        
        #   Composite thermal conductivity [W/m.K]
        self.k_comp = _np.add(
                _np.multiply(self.f_cu, k_cu), _np.multiply(self.f_sc, k_sc)
                )

        #   Average composite thermal conductivity [W/m.K]
        self.avg_k_comp = _np.add(
                _np.multiply(self.f_cu, avg_k_cu), _np.multiply(self.f_sc, avg_k_sc)
                )

        self.Jop = _np.divide(Iop, self.s_cu + self.s_sc)

    def calc_area_sc_cu(self, d_cond, ratio_cu_sc, d_isolation=0.0):
        try:
            d_cond = _np.subtract(d_cond, d_isolation)
            s_cond = _np.multiply(_np.pi, _np.power(d_cond*0.5, 2))
            s_sc = _np.divide(s_cond, _np.add(ratio_cu_sc, 1))
            s_cu = _np.subtract(s_cond, s_sc)
            return [s_sc, s_cu]
        except Exception:
            _traceback.print_exc(file=_sys.stdout)

    def calc_ratio_cu_sc(self, d_cond, s_sc, d_isolation=0.0):
        try:
            d_cond = _np.subtract(d_cond, d_isolation)
            s_cond = _np.multiply(_np.pi, _np.power(d_cond*0.5, 2))
            s_cu = _np.subtract(s_cond, s_sc)
            ratio_cu_sc = _np.subtract(_np.divide(s_cond, s_sc), 1)
            return [ratio_cu_sc, s_cu]
        except Exception:
            _traceback.print_exc(file=_sys.stdout)



def calc_ratio_cu_sc(d_cond, s_sc, d_isolation=0.0):
    try:
        d_cond = _np.subtract(d_cond, d_isolation)
        s_cond = _np.multiply(_np.pi, _np.power(d_cond*0.5, 2))
        s_cu = _np.subtract(s_cond, s_sc)
        ratio_cu_sc = _np.subtract(_np.divide(s_cond, s_sc), 1)
        return [ratio_cu_sc, s_cu]
    except Exception:
        _traceback.print_exc(file=_sys.stdout)

def calc_area_sc_cu(d_cond, ratio_cu_sc, d_isolation=0.0):
    try:
        d_cond = _np.subtract(d_cond, d_isolation)
        s_cond = _np.multiply(_np.pi, _np.power(d_cond*0.5, 2))
        s_sc = _np.divide(s_cond, _np.add(ratio_cu_sc, 1))
        s_cu = _np.subtract(s_cond, s_sc)
        return [s_sc, s_cu]
    except Exception:
        _traceback.print_exc(file=_sys.stdout)

if __name__ == "__main__":

    copper = Copper()
    nbti = NbTi()
    
    #T = 9.2
    #RRR = 100

    print('\n Enter operation parameters:')
    T = _np.float_(input('\n    Temperature [K]: '))
    RRR = int(input('\n    Copper RRR: '))

    print('\n T = {} K'.format(T))
    print(' RRR = {}'.format(RRR))

    [rho,c,k] = copper.calc_properties(T, RRR)

    print('\n Copper Properties:')
    print('\n    Resistivity: {} Ohm.m'.format(rho))
    print('    Specific heat: {} J/Kg.K'.format(c))
    print('    Thermal conductivity: {} W/m.K'.format(k))
    
    print('\n NbTi Properties:')
    print('\n    Specific heat: {} J/kg.K\n'.format(
                                        nbti.calc_specific_heat(T,0,True)))
    print('    Thermal conductivity: {} W/m.K'.format(
                                        nbti.calc_thermal_conductivity(T)))

    ## Plot resistivity
    for rrr in copper._thermal_conductivity_per_rrr_data.keys():
        plt.loglog( copper._specific_heat_data['T'],
                    [copper.calc_resistivity(t, rrr, 0) 
                    for t in copper._specific_heat_data['T'] ]
        )
        
    plt.legend(copper._thermal_conductivity_per_rrr_data.keys(), title='RRR')
    plt.grid(which='both')
    plt.title('Electrical resistivity of copper')
    plt.xlabel('Temperature [K]')
    plt.ylabel('Resistivity [Ohm.m]')
    plt.show()
    
    ## Plot thermal conductivity
    T_array = [_np.float_(i) for i in range(4,300)]

    for i in copper._thermal_conductivity_per_rrr_data.keys():
        plt.loglog( copper._thermal_conductivity_per_rrr_data[i]['T'],
                    copper._thermal_conductivity_per_rrr_data[i]['k'])

    plt.loglog( T_array,
                [nbti.calc_thermal_conductivity(t) for t in T_array ]
        )

    k_legends = list(copper._thermal_conductivity_per_rrr_data.keys())
    k_legends = ['Cu RRR ' + str(rrr)
                    for rrr in copper._thermal_conductivity_per_rrr_data.keys()]
    k_legends.append('Nb-Ti')
    plt.legend(k_legends)
    plt.grid(which='both')
    plt.title('Thermal conductivity of copper and Nb-Ti')
    plt.xlabel('Temperature [K]')
    plt.ylabel('Thermal conductivity [W/m.K]')
    plt.show()

    ## Plot specific heat
    T_array = _np.sort(_np.append(
                        copper._specific_heat_data['T'], 
                        [4.0 + i/10.0 for i in range(60)]
                    )
                )

    plt.plot( copper._specific_heat_data['T'],
                copper._specific_heat_data['c'],'x-')

    plt.plot( T_array,
                [nbti.calc_specific_heat(t, 0, True) for t in T_array ],'x-'
        )
    plt.plot( T_array,
                [nbti.calc_specific_heat(t, 6, True) for t in T_array ],'x-'
        )
    plt.plot( T_array,
                [nbti.calc_specific_heat(t, 0, False) for t in T_array ],'x-'
        )
    #'''

    plt.grid(which='both')
    plt.title('Specific heat of copper and NbTi')
    plt.legend(['Copper',
                'Superconducting Nb-Ti, B = 0 T',
                'Superconducting Nb-Ti, B = 0 T',
                'Normal conducting Nb-Ti'])
    plt.xlabel('Temperature [K]')
    plt.ylabel('Specific Heat [J/kg.K]')
    plt.show()

