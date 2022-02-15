import matplotlib.pyplot as _plt
import numpy as _np
import sys as _sys
import traceback as _traceback

import materials as _materials

def calc_detection_voltage(vq,rho,tqd,Io,Acu):
    try:
        if type(vq) == _np.ndarray:
            vdets = []
            for v in vq:
                R = _np.multiply(_np.multiply(v, tqd), _np.divide(rho, Acu))
                vdet = _np.multiply(R, Io)
                vdets.append(vdet)
            return vdets

        else:
            R = _np.multiply(_np.multiply(vq, tqd), _np.divide(rho, Acu))
            return _np.multiply(R, Io)
    except Exception:
        _traceback.print_exc(file=_sys.stdout)

def calc_prop_velocity(Jo, C, rho, k, Tjoule, Top, method):
    try:
        v = _np.multiply(
                _np.divide(Jo,C),
                _np.sqrt(
                    _np.divide(
                        _np.multiply(rho,k),
                        _np.subtract(Tjoule,Top)
                    )
                )
            )
        if method == "adiabatic":
            prop_vel = v
        elif method == "cooled":
            corr_factor = 0.0
            prop_vel = _np.multiply(corr_factor, v)
        else:
            prop_vel = 5
        return prop_vel
    except Exception:
        _traceback.print_exc(file=_sys.stdout)

def prop_velocity_estimations(parameters: dict):
    
    [Iop, B, Top, Tc, Tcs, RRR, ratio_cu_sc, d_cond] = parameters.values()

    # Transition temperature [k]
    Tjoule = _np.divide(_np.add(Tc, Tcs), 2)
    
    # Total conductor and composite areas [mm²]
    s_cond = _np.multiply(_np.pi, _np.power(_np.divide(d_cond, 2), 2))
    [s_sc, s_cu] = _materials.calc_area_sc_cu(d_cond, ratio_cu_sc)
    
    print('\n ### Calculated properties ###')
    print('\n    Tjoule = {} K'.format(Tjoule))
    print('    SC area = {} mm²'.format(s_sc))
    print('    Copper area = {} mm²'.format(s_cu))
 
    """ Copper properties @ Tjoule """
    copper = _materials.Copper()

    # Copper fraction
    f_cu = _np.divide(s_cu, s_cond)

    # Resistivity [Ohm.m]
    # Specific heat [J/kg.K]
    # Thermal conductivity [W/m.K]
    # Density [kg/m³]
    [resty_cu, c_cu, k_cu] = copper.calc_properties(Tjoule, RRR, B)
    dsty_cu = copper.density

    """ Nb-Ti properties @ Tjoule """
    nbti = _materials.NbTi()
    
    # Nb-Ti fraction
    f_sc = _np.divide(s_sc, s_cond)

    # Resistivity [Ohm.m]
    # Specific heat [J/kg.K]
    # Thermal conductivity [W/m.K] - ref.: "Thermal Conductivity and Electrical
    #                           Resistivity of NbTi Alloys at Low Temperatures"
    # Density [kg/m³]
    resty_sc = 1e-5
    c_sc = nbti.calc_specific_heat(Tjoule)
    c_sc = [2.414, 3.85, 5.391]
    #c_sc = 2.414
    k_sc = 0.5              
    dsty_sc = nbti.density

    print('\n    Copper specific heat = {} J/kg.K'.format(c_cu))
    print('    SC specific heat = {} J/kg.K'.format(c_sc))
    
    # Current density. During quench, all current goes to copper.
    #Jop = _np.divide(_np.multiply(Iop, 1e6), s_cu)
    Jop = _np.divide(_np.multiply(Iop, 1e6), s_cu + s_sc)

    # Composite volumetric specific heat
    C_comp = _np.add(
        _np.multiply(_np.multiply(f_cu, dsty_cu), c_cu),
        _np.multiply(_np.multiply(f_sc, dsty_sc), c_sc)
        )
    #C_comp = dsty_cu*c_cu;

    # Composite resistivity
    resty_comp = _np.divide(
        1,
        _np.add(
            _np.divide(f_cu, resty_cu),
            _np.divide(f_sc, resty_sc)
            )
        )
    # Composite thermal conductivity
    k_comp = _np.add(_np.multiply(f_cu, k_cu), _np.multiply(f_sc, k_sc))

    print('\n    Composite volumetric specific heat = {} J/kg.K'.format(C_comp))
    print('    Copper volumetric specific heat = {} J/kg.K'.format(
                                                                dsty_cu*c_cu))
    print('\n    Composite thermal conductivity = {} W/m.K'.format(k_comp))
    print('    Copper thermal conductivity = {} W/m.K'.format(k_cu))

    print('\n    Composite resistivity = {} Ohm.m'.format(resty_comp))
    print('    Copper resistivity = {} Ohm.m'.format(resty_cu))

    # Velocity estimation
    method = 'adiabatic'
    vqs = calc_prop_velocity(
                Jop, C_comp, resty_comp, k_comp, Tjoule, Top, method
        )
    
    print('\n    Propagation velocity = {} m/s\n\n'.format(vqs))

    
    tqd = [t*0.1/100 for t in range(100)]

    #vdet_comp = calc_detection_voltage(vqs,resty_comp,tqd,Iop,s_cond*1e-6)
    vdet_cu = calc_detection_voltage(vqs,resty_cu,tqd,Iop,s_cu*1e-6)

    for vd in vdet_cu:
        _plt.plot(tqd,vd)

    _plt.title(
            'Estimated detection voltage @ Iop = {} A, Top = {} K, RRR = {}, Ratio Cu/Nb-Ti = {}'.format(
                parameters['Iop'],
                parameters['Top'],
                parameters['RRR'],
                parameters['ratio_cu_sc'])
        )

    _plt.legend([2.414, 3.85, 5.391], title = 'NbTi specific heat')

    _plt.xlabel('Time [s]')
    _plt.ylabel('Detection voltage [V]')
    _plt.grid()
    _plt.show()

    return vqs
    