import sys as _sys
import traceback as _traceback
import numpy as _np

# def copper_properties(T,RRR,B):
#     """
#        Refs.: 
#        [1] M. McAshan, "MIITS Integrals for Copper and for Nb-46Ti"
#        [2] KN5010 Nº4 (Davide)
#        [3] https://www.copper.org/resources/properties/cryogenic/   """
#     # Resistivity [Ohm.m]
#     rho = _np.multiply(
#             1e-8,
#             _np.add(
#                 _np.divide(1.545,RRR),
#                 _np.divide(
#                     1,
#                     _np.add(
#                         _np.add(
#                             _np.divide(2.32547*1e9, _np.power(T,5)),
#                             _np.divide(9.57137*1e5, _np.power(T,3))
#                             ),
#                         _np.divide(1.62735*1e2, T)
#                         )
#                     )
#                 )
#             )
#     # Specific heat [J/kg.K] - polynomial fit obtained for temperatures up to 50 K
#     P = [-0.000006646433277, 0.001186241294937, -0.003070534537926, 0.018727649162436, 0]
#     c = _np.polyval(P,T)
#     # Thermal conductivity [W/m.K]
#     k = 
#     return [rho, c, k]

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