#!/usr/bin/env python

import detection as _detection
import materials as _materials
import quench as _quench

import numpy as _np
import matplotlib.pyplot as _plt

### Operation parameters for high-field
dict_high_field_parameters = {

    # Operating current [A]
    'Iop' : 250,

    # Operating field [T]
    'B' : 5.09,

    # Operating SC temperature [K]
    'Top' : 5.0,

    # Critical temperature [K]
    'Tc' : 9.2,

    # Current-sharing temperature [K]
    'Tcs' : 5.95,

    # Residual resistivity ratio
    'RRR' : 50,

    # Cu/Nb-Ti ratio
    'ratio_cu_sc' : 1.2,

    # Total conductor diameter [m]
    'd_cond' : 8.2e-4
}

# Maximum voltage across dump resistor [V]
Vmax = 600
# Magnet Inductance [H]
L = 0.116

figure_size = [9.6, 7.2]

if __name__ == "__main__":
  
    print('\n\n *** Protection results ***\n')

    #t_switch_list = [0, 0.025, 0.05, 0.075, 0.1, 0.125, 0.15, 0.175, 2.0]
    ratio_list = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2]
    t_switch = 0.1

    miits = []

    R = _quench.calc_resistor(dict_high_field_parameters['Iop'], Vmax)
    tau = L/R
    for ratio in ratio_list:
        dict_high_field_parameters['ratio_cu_sc'] = ratio
        wire = _materials.SCWire(dict_high_field_parameters)
        miits.append(
            _quench.calc_hot_spot(
                wire.s_cu,
                wire.s_sc,
                dict_high_field_parameters['Iop'],
                tau,
                t_switch,
                dict_high_field_parameters['RRR']
            )
        )


    print(' Results for Model 3\n')
    print('    R = {} ohm'.format(R))
    print('    tau = {}'.format(tau))

    _plt.figure(figsize=figure_size)
    _plt.plot(ratio_list, miits, '--x')

    _plt.title(
            'Hot-spot estimate @ Iop = {} A, RRR = {}, L = {} H, R_dump = {} ohm'.format(
                dict_high_field_parameters['Iop'],
                dict_high_field_parameters['RRR'],
                L,
                R)
        )

    _plt.xlabel('Cu/Nb-Ti')
    _plt.ylabel('T_max [K]')
    _plt.minorticks_on()
    _plt.grid(which='both', axis='both')
    _plt.show()
