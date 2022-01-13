from re import T
import numpy as _np
import matplotlib.pyplot as plt
import sys as _sys
import traceback as _traceback

from numpy.core.defchararray import array

class Copper:
    """ Class to hold copper properties 
    
        Refs.: 
        [1] M. McAshan, "MIITS Integrals for Copper and for Nb-46Ti"
        [2] KN5010 Nº4 (Davide)
        [3] https://www.copper.org/resources/properties/cryogenic/   
    """

    def __init__(self):    

        
        self._specific_heat_data = {
            'T':
                _np.array([4, 6, 8, 10, 12, 14, 16, 18, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300]),

            'c': _np.array([0.09942, 0.2303, 0.4639, 0.8558, 1.47, 2.375, 3.64, 5.327, 7.491, 26.4, 57.63, 95.84, 135.2, 171.8, 203.8, 230.9, 253.5, 287.6, 311.6, 329.4, 343.4, 355, 364.7, 372.6, 378.6, 382.5, 384])
        }

        self._thermal_conductivity_per_rrr_data = {
            50: {
                'T': 
                    _np.array([4, 6, 8, 10, 12, 14, 16, 18, 20, 30, 40, 50, 60, 70, 80, 90,  100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300]),

                'k':
                    _np.array([320.4, 466.8, 622.3, 778.1, 927.3, 1064.0, 1185.0, 1287.0, 1368.0, 1444.0, 1163.0, 863.6, 670.0, 561.1, 500.3, 465.1, 443.9, 421.8, 411.6, 406.0, 402.6, 400.1, 398.2, 396.5, 395.0, 393.6, 392.4])
            },

            100: {
                'T': 
                    _np.array([4, 6, 8, 10, 12, 14, 16, 18, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300]),

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
                    _np.array([4, 6, 8, 10, 12, 14, 16, 18, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300]),

                'k':
                    _np.array([1926.6, 2810.0, 3636.0, 4320.0, 4829.0, 5147.0, 5276.0, 5234.0, 5052.0, 3257.0, 1833.0, 1130.0, 801.8, 638.5, 551.0, 501.0, 471.1, 440.6, 427.6, 421.2, 417.5, 414.6, 411.8, 408.8, 405.5, 401.8, 397.9])
            }
        }

    def calc_resistivity(self, T, RRR, B):
    # Ref.: M. McAshan, "MIITS Integrals for Copper and for Nb-46Ti "
        return _np.multiply(
            1e-8,
            _np.add(
                _np.divide(1.545, RRR),
                _np.divide(
                    1,
                    _np.add(
                        _np.add(
                            _np.divide(2.32547*1e9, _np.power(T, 5)),
                            _np.divide(9.57137*1e5, _np.power(T, 3))
                            ),
                        _np.divide(1.62735*1e2, T)
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

    def calc_thermal_conductivity(self, T, RRR):
        
        return _np.interp(
            T,
            self._thermal_conductivity_per_rrr_data[RRR]['T'],
            self._thermal_conductivity_per_rrr_data[RRR]['k']
            )

    def calc_properties(self, T, RRR, B = 0):
        
        rho = self.calc_resistivity(T, RRR, B)      # [Ohm.m]
        c = self.calc_specific_heat(T)              # [J/kg.K]
        k = self.calc_thermal_conductivity(T, RRR)  # [W/m.K]

        return [rho, c, k]


class NbTi:

    def __init__(self):

        self._specific_heat_data = {

            'T':
                _np.array([1.0500, 1.5000, 2.0143, 2.5071, 3.0429, 3.5143, 4.0286, 4.5000, 5.0357, 5.5500, 6.0210, 6.5571, 7.0071, 7.5214, 8.0143, 8.5286, 9.0214]),

            'c':
                _np.array([0.0743, 0.0850, 0.0957, 0.1129, 0.1321, 0.1514, 0.1750, 0.1986, 0.2264, 0.2521, 0.2779, 0.3079, 0.3314, 0.3614, 0.3850, 0.4107, 0.4343])
        }

    def calc_specific_heat(self, T):
        return _np.interp(
            T,
            self._specific_heat_data['T'],
            self._specific_heat_data['c']
            )

class SCWire:
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

    T = 9.2
    RRR = 100
    print('\nT = {} K'.format(T))
    print('RRR = {}'.format(RRR))

    [rho,c,k] = copper.calc_properties(T, RRR)

    print('\n Copper Properties:')
    print('\n    Resistivity: {} Ohm.m'.format(rho))
    print('    Specific heat: {} J/Kg.K'.format(c))
    print('    Thermal conductivity: {} W/m.K'.format(k))
    
    print('\n NbTi Properties:')
    print('\n    Specific heat: {} J/kg.K\n'.format(nbti.calc_specific_heat(T)))

    # Plot resistivity
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
    
    # Plot thermal conductivity
    for i in copper._thermal_conductivity_per_rrr_data.keys():
        plt.loglog( copper._thermal_conductivity_per_rrr_data[i]['T'],
                    copper._thermal_conductivity_per_rrr_data[i]['k'])

    plt.legend(copper._thermal_conductivity_per_rrr_data.keys(), title='RRR')
    plt.grid(which='both')
    plt.axis([4,300,100,10000])
    plt.title('Thermal conductivity of copper')
    plt.xlabel('Temperature [K]')
    plt.ylabel('Thermal conductivity [W/m.K]')
    plt.show()

    # Plot specific heat
    plt.loglog( copper._specific_heat_data['T'],
                copper._specific_heat_data['c'])
    plt.loglog( nbti._specific_heat_data['T'],
                nbti._specific_heat_data['c'])
    plt.grid(which='both')
    plt.title('Specific heat of copper and NbTi')
    plt.legend(['Copper','NbTi'])
    plt.xlabel('Temperature [K]')
    plt.ylabel('Specific Heat [J/kg.K]')
    plt.show()