#!/usr/bin/env python

import detection as _detection
import materials as _materials

import numpy as _np
import matplotlib.pyplot as _plt

### Operation parameters for high-field
dict_high_field_parameters = {

    # Operating current [A]
    'Iop' : 360,

    # Operating field [T]
    'B' : 0,

    # Operating SC temperature [K]
    'Top' : 4.2,

    # Critical temperature [K]
    'Tc' : 9.2,

    # Current-sharing temperature [K]
    'Tcs' : 5.47,

    # Residual resistivity ratio
    'RRR' : 100,

    # Cu/Nb-Ti ratio
    'ratio_cu_sc' : 0.886,

    # Total conductor diameter [m]
    'd_cond' : 8.2e-4,

    # Magnet inductance [H]
    'L' : 0.02
}
    
if __name__ == "__main__":
  
    Bs = [0,5.55]
    RRRs = [50,100]

    print('\n\n *** Propagation and detection results ***\n')

    plot_legend = []

    for rrr in RRRs:
        for b in Bs:
        
            dict_high_field_parameters['B'] = b
            dict_high_field_parameters['RRR'] = rrr
            
            wire = _materials.SCWire(dict_high_field_parameters)

            # Velocity estimation based on composite material properties
            method = 'adiabatic'
            vqs = _detection.calc_prop_velocity(
                        wire.Jop, 
                        wire.avg_C_comp, 
                        wire.resty_comp, 
                        wire.avg_k_comp, 
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

            str_cond = 'RRR = {}, B = {} T'.format(rrr,b)

            print(' Results for ' + str_cond + '\n')
            print('    Propagation velocity = {} m/s'.format(vqs))
            print('    Detection voltage @ {} ms = {} V \n\n'.format(t_det*1e3, vdet_t))

            
            # Time evolution simulation
            tqd = [t*0.1/100 for t in range(100)]
            vdet_qd = _detection.calc_detection_voltage(
                        vqs,
                        wire.resty_comp,
                        tqd,
                        dict_high_field_parameters['Iop'],
                        wire.s_cond)
            
            _plt.plot(tqd,vdet_qd)
            plot_legend.append(str_cond)

    _plt.title(
            'Estimated detection voltage @ Iop = {} A, Top = {} K, Tcs = {} K, Ratio Cu/Nb-Ti = {}'.format(
                dict_high_field_parameters['Iop'],
                dict_high_field_parameters['Top'],
                dict_high_field_parameters['Tcs'],
                dict_high_field_parameters['ratio_cu_sc'])
        )

    _plt.legend(plot_legend)
    _plt.xlabel('Time [s]')
    _plt.ylabel('Detection voltage [V]')
    _plt.grid()
    _plt.show()
