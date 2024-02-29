#!/usr/bin/env python

import detection as _detection
import materials as _materials

import numpy as _np
import matplotlib.pyplot as _plt

### Operation parameters for high-field
dict_high_field_parameters = {

    # Operating current [A]
    'Iop' : 275,

    # Operating field [T]
    'B' : [0, 6],

    # Operating SC temperature [K]
    'Top' : 4.2,

    # Critical temperature [K]
    'Tc' : 9.2,

    # Current-sharing temperature [K]
    'Tcs' : 6.06,

    # Residual resistivity ratio
    'RRR' : 50,

    # Cu/Nb-Ti ratio
    'ratio_cu_sc' : 0.9,

    # Total conductor diameter [m]
    'd_cond' : 0.85e-3,

    # Magnet inductance [H]
    'L' : 0.0997
}
    
if __name__ == "__main__":
  
    wire = _materials.SCWire(dict_high_field_parameters)

    print('\n *** Operation conditions ***\n')
    for i in dict_high_field_parameters.items():
        print(i)
    
    print('\n\n *** Wire initialization ***\n')
    for i in vars(wire).items():
        print(i)
    
    # Velocity estimation based on composite material properties
    method = 'adiabatic'
    vqs = _detection.calc_prop_velocity(
                wire.Jop, 
                wire.C_comp, 
                wire.resty_comp, 
                wire.k_comp, 
                wire.Tjoule, 
                dict_high_field_parameters['Top'], 
                'adiabatic'
        )

    # Detection time [s]
    t_det = 0.05

    # Detection voltage for specified detection time [V]
    vdet_t = _detection.calc_detection_voltage(
                vqs,
                wire.resty_comp,
                t_det,
                dict_high_field_parameters['Iop'],
                wire.s_cond)

    print('\n\n *** Propagation and detection results ***\n')
    print('    Propagation velocity = {} m/s'.format(vqs))
    print('    Detection voltage @ {} ms = {} V \n\n'.format(t_det*1e3, vdet_t))

    
    # Time evolution simulation
    tqd = [t*0.1/100 for t in range(100)]
    vdet_comp = _detection.calc_detection_voltage(
                vqs,
                wire.resty_comp,
                tqd,
                dict_high_field_parameters['Iop'],
                wire.s_cond)
    
    if vdet_comp.ndim > 1:
        for vd in vdet_comp:
            _plt.plot(tqd,vd)
    else:
        _plt.plot(tqd,vdet_comp)

    _plt.title(
            'Estimated detection voltage @ Iop = {} A, Top = {} K, RRR = {}, Ratio Cu/Nb-Ti = {}'.format(
                dict_high_field_parameters['Iop'],
                dict_high_field_parameters['Top'],
                dict_high_field_parameters['RRR'],
                dict_high_field_parameters['ratio_cu_sc'])
        )

    _plt.legend(
        ['{} T'.format(b) for b in dict_high_field_parameters['B']], 
        title = 'Magnetic field on wire')
    _plt.xlabel('Time [s]')
    _plt.ylabel('Detection voltage [V]')
    _plt.grid()
    _plt.show()
