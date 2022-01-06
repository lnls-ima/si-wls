import sys as _sys
import traceback as _traceback
import numpy as _np

class Copper:
    """ Class to hold copper properties """

    def __init__(self):
        self.thermal_conductivity_data_at_rrr_50 = _np.array(
            [
            [4, 320.4],
            [6, 466.8],
            [8, 622.3],
            [10, 778.1],
            [12, 927.3],
            [14, 1064.0],
            [16, 1185.0],
            [18, 1287.0],
            [20, 1368.0],
            [30, 1444.0],
            [40, 1163.0],
            [50, 863.6],
            [60, 670.0],
            [70, 561.1],
            [80, 500.3],
            [90, 465.1],
            [100, 443.9],
            [120, 421.8],
            [140, 411.6],
            [160, 406.0],
            [180, 402.6],
            [200, 400.1],
            [220, 398.2],
            [240, 396.5],
            [260, 395.0],
            [280, 393.6],
            [300, 392.4]
        ])
        self.thermal_conductivity_data_at_rrr_100 = _np.array(
            [
            [4, 642.3],
            [6, 931.7],
            [8, 1239.0],
            [10, 1540.0],
            [12, 1814.0],
            [14, 2045.0],
            [16, 2226.0],
            [18, 2352.0],
            [20, 2423.0],
            [30, 2143.0],
            [40, 1485.0],
            [50, 1005.0],
            [60, 741.2],
            [70, 603.6],
            [80, 529.3],
            [90, 487.0],
            [100, 461.5],
            [120, 434.8],
            [140, 422.1],
            [160, 415.0],
            [180, 410.3],
            [200, 407.0],
            [220, 404.2],
            [240, 401.9],
            [260, 399.9],
            [280, 398.0],
            [300, 396.3]
        ])
        self.thermal_conductivity_data_at_rrr_200 = _np.array(
            [
            [3.9415, 1284.10],
            [4.0000, 1311.10],
            [4.8801, 1631.80],
            [5.3705, 1830.00],
            [6.0423, 2073.70],
            [7.0531, 2399.30],
            [8.3552, 2747.40],
            [9.3312, 2986.20],
            [10.8120, 3279.70],
            [12.0750, 3455.10],
            [14.6240, 3678.00],
            [16.5750, 3755.40],
            [18.5110, 3716.50],
            [20.0740, 3639.90],
            [30.7730, 2580.90],
            [40.7130, 1631.80],
            [50.0380, 1075.70],
            [60.1550, 803.48],
            [70.2180, 652.35],
            [80.1740, 569.71],
            [90.2020, 518.72],
            [100.0000, 487.28],
            [120.2200, 462.55],
            [140.3300, 443.67],
            [161.4100, 430.02],
            [180.2700, 425.56],
            [201.3300, 416.78],
            [249.2700, 408.19]
        ])
        self.thermal_conductivity_data_at_rrr_300 = _np.array(
            [
            [6, 2810.0],
            [8, 3636.0],
            [10, 4320.0],
            [12, 4829.0],
            [14, 5147.0],
            [16, 5276.0],
            [18, 5234.0],
            [20, 5052.0],
            [30, 3257.0],
            [40, 1833.0],
            [50, 1130.0],
            [60, 801.8],
            [70, 638.5],
            [80, 551.0],
            [90, 501.0],
            [100, 471.1],
            [120, 440.6],
            [140, 427.6],
            [160, 421.2],
            [180, 417.5],
            [200, 414.6],
            [220, 411.8],
            [240, 408.8],
            [260, 405.5],
            [280, 401.8],
            [300, 397.9]
        ])

def copper_properties(T,RRR,B):
    """
       Refs.: 
       [1] M. McAshan, "MIITS Integrals for Copper and for Nb-46Ti"
       [2] KN5010 Nº4 (Davide)
       [3] https://www.copper.org/resources/properties/cryogenic/   """
    # Resistivity [Ohm.m]
    rho = _np.multiply(
            1e-8,
            _np.add(
                _np.divide(1.545,RRR),
                _np.divide(
                    1,
                    _np.add(
                        _np.add(
                            _np.divide(2.32547*1e9, _np.power(T,5)),
                            _np.divide(9.57137*1e5, _np.power(T,3))
                            ),
                        _np.divide(1.62735*1e2, T)
                        )
                    )
                )
            )
    # Specific heat [J/kg.K] - polynomial fit obtained for temperatures up to 50 K
    P = [-0.000006646433277, 0.001186241294937, -0.003070534537926, 0.018727649162436, 0]
    c = _np.polyval(P,T)
    # Thermal conductivity [W/m.K]
    k = 0 # dummy value
    return [rho, c, k]

def copper_resistivity(T, RRR):
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
