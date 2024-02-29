#!/usr/bin/env python

import detection as _detection
import materials as _materials
import quench as _quench

import numpy as _np
import matplotlib.pyplot as _plt

"""
This script estimates the hot-spot temperature for
two operating current scenarios of Model 6: 240 and 300 A.

The impact of increasing the maximum voltage across the
dump resistor is also analysed.
"""

# Maximum voltage across dump resistor [V]
Vmin = 600
Vmax = 800
# Magnet Inductance [H]
L = 0.108

I_min = 240
I_max = 300

# variable inductance
L_I = {
    0: 0.300,
    24: 0.2583,
    48: 0.1899,
    72: 0.1558,
    96: 0.13563,
    120: 0.1256,
    144: 0.1188,
    168: 0.1142,
    192: 0.1109,
    216: 0.1084,
    240: 0.1065
    }

### Operation parameters for high-field
dict_high_field_parameters = {

    # Operating current [A]
    'Iop' : 240,

    # Operating field [T]
    'B' : 5.33,

    # Operating SC temperature [K]
    'Top' : 5.0,

    # Critical temperature [K]
    'Tc' : 9.2,

    # Current-sharing temperature [K]
    'Tcs' : 6.08,

    # Residual resistivity ratio
    'RRR' : 50,

    # Cu/Nb-Ti ratio
    'ratio_cu_sc' : 0.9,

    # Total conductor diameter [m]
    'd_cond' : 8.5e-4,

    'L' : L_I
}

figure_size = [9.6, 7.2]

if __name__ == "__main__":
  
    print('\n\n *** Protection results ***\n')

    t_switch_list = [0, 0.025, 0.05, 0.075, 0.1, 0.125, 0.15, 0.175, 0.2]
    #ratio_list = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2]

    hotspot_300A_600V = []
    hotspot_240A_600V = []
    hotspot_300A_800V = []
    hotspot_240A_800V = []

    wire = _materials.SCWire(dict_high_field_parameters)

    R = _quench.calc_resistor(I_max, Vmin)
    tau = L/R
    R2 = _quench.calc_resistor(I_max, Vmax)
    tau2 = L/R2
    for t_switch in t_switch_list:
        hotspot_240A_600V.append(
            _quench.calc_hot_spot(
                wire.s_cu,
                wire.s_sc,
                I_min,
                tau,
                t_switch,
                dict_high_field_parameters['RRR']
            )
        )
    for t_switch in t_switch_list:
        hotspot_300A_600V.append(
            _quench.calc_hot_spot(
                wire.s_cu,
                wire.s_sc,
                I_max,
                tau,
                t_switch,
                dict_high_field_parameters['RRR']
            )
        )
    for t_switch in t_switch_list:
        hotspot_240A_800V.append(
            _quench.calc_hot_spot(
                wire.s_cu,
                wire.s_sc,
                I_min,
                tau2,
                t_switch,
                dict_high_field_parameters['RRR']
            )
        )
    for t_switch in t_switch_list:
        hotspot_300A_800V.append(
            _quench.calc_hot_spot(
                wire.s_cu,
                wire.s_sc,
                I_max,
                tau2,
                t_switch,
                dict_high_field_parameters['RRR']
            )
        )


    print(' Results for Model 6\n')
    print('    R = {} ohm'.format(R))
    print('    tau = {}'.format(tau))
    print('    R2 = {} ohm'.format(R2))
    print('    tau2 = {}'.format(tau2))

    _plt.figure(figsize=figure_size)
    _plt.plot(t_switch_list, hotspot_240A_600V, '--x')
    _plt.plot(t_switch_list, hotspot_300A_600V, '--x')
    _plt.plot(t_switch_list, hotspot_240A_800V, '--x')
    _plt.plot(t_switch_list, hotspot_300A_800V, '--x')

    _plt.title(
            'Hot-spot estimate @ Iop = {}/{} A, RRR = {}, L = {:.3f} H'.format(
                240,
                300,
                dict_high_field_parameters['RRR'],
                L)
        )
    _plt.legend(
        [
            '{} A, {:.2f} Ohm, {} V'.format(I_min, R, I_min*R),
            '{} A, {:.2f} Ohm, {} V'.format(I_max, R, I_max*R),
            '{} A, {:.2f} Ohm, {} V'.format(I_min, R2, I_min*R2),
            '{} A, {:.2f} Ohm, {} V'.format(I_max, R2, I_max*R2)
            ]
    )

    _plt.xlabel('t_prot [s]')
    _plt.ylabel('T_max [K]')
    _plt.minorticks_on()
    _plt.grid(which='both', axis='both')
    _plt.show()
