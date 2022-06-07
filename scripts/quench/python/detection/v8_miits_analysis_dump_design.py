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
L = 0.122

I_min = 228
I_max = 300

### Operation parameters for high-field
dict_high_field_parameters = {

    # Operating current [A]
    'Iop' : I_min,

    # Operating field [T]
    'B' : 5.30,

    # Operating SC temperature [K]
    'Top' : 5.0,

    # Critical temperature [K]
    'Tc' : 9.2,

    # Current-sharing temperature [K]
    'Tcs' : 6.1,

    # Residual resistivity ratio
    'RRR' : 50,

    # Cu/Nb-Ti ratio
    'ratio_cu_sc' : 0.97,

    # Total conductor diameter [m]
    'd_cond' : 8.5e-4,

    'L' : L
}

figure_size = [9.6, 7.2]

if __name__ == "__main__":
  
    print('\n\n *** Protection results ***\n')

    t_switch_list = [0, 0.025, 0.05, 0.075, 0.1, 0.125, 0.15, 0.175, 0.2]
    #ratio_list = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2]

    hotspot_Imin_Vmin = []
    hotspot_Imax_Vmin = []
    hotspot_Imin_Vmax = []
    hotspot_Imax_Vmax = []

    wire = _materials.SCWire(dict_high_field_parameters)

    R1 = _quench.calc_resistor(I_max, Vmin)
    tau1 = L/R1
    R2 = _quench.calc_resistor(I_max, Vmax)
    tau2 = L/R2
    for t_switch in t_switch_list:
        hotspot_Imin_Vmin.append(
            _quench.calc_hot_spot(
                wire.s_cu,
                wire.s_sc,
                I_min,
                tau1,
                t_switch,
                dict_high_field_parameters['RRR']
            )
        )
    for t_switch in t_switch_list:
        hotspot_Imax_Vmin.append(
            _quench.calc_hot_spot(
                wire.s_cu,
                wire.s_sc,
                I_max,
                tau1,
                t_switch,
                dict_high_field_parameters['RRR']
            )
        )
    for t_switch in t_switch_list:
        hotspot_Imin_Vmax.append(
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
        hotspot_Imax_Vmax.append(
            _quench.calc_hot_spot(
                wire.s_cu,
                wire.s_sc,
                I_max,
                tau2,
                t_switch,
                dict_high_field_parameters['RRR']
            )
        )


    print(' Results for Model 8\n')
    print('    R = {} ohm'.format(R1))
    print('    tau = {}'.format(tau1))
    print('    R2 = {} ohm'.format(R2))
    print('    tau2 = {}'.format(tau2))

    _plt.figure(figsize=figure_size)
    _plt.plot(t_switch_list, hotspot_Imin_Vmin, '--x')
    _plt.plot(t_switch_list, hotspot_Imax_Vmin, '--x')
    _plt.plot(t_switch_list, hotspot_Imin_Vmax, '--x')
    _plt.plot(t_switch_list, hotspot_Imax_Vmax, '--x')

    _plt.title(
            'Hot-spot estimate @ Iop = {}/{} A, RRR = {}, L = {:.3f} H'.format(
                I_min,
                I_max,
                dict_high_field_parameters['RRR'],
                L)
        )
    _plt.legend(
        [
            '{} A, {:.2f} Ohm, {} V'.format(I_min, R1, I_min*R1),
            '{} A, {:.2f} Ohm, {} V'.format(I_max, R1, I_max*R1),
            '{} A, {:.2f} Ohm, {} V'.format(I_min, R2, I_min*R2),
            '{} A, {:.2f} Ohm, {} V'.format(I_max, R2, I_max*R2)
            ]
    )

    _plt.xlabel('t_prot [s]')
    _plt.ylabel('T_max [K]')
    _plt.minorticks_on()
    _plt.grid(which='both', axis='both')
    _plt.show()
