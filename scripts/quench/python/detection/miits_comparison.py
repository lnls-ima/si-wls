#!/usr/bin/env python

import detection as _detection
import materials as _materials
import quench as _quench

import numpy as _np
import matplotlib.pyplot as _plt

### Operation parameters for high-field
dict_high_field_parameters = {

    'A_50' : 
    {
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

        # Magnet inductance [H]
        'L' : 0.108
    },

    'A_100' : 
    {
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
        'RRR' : 100,

        # Cu/Nb-Ti ratio
        'ratio_cu_sc' : 0.9,

        # Total conductor diameter [m]
        'd_cond' : 8.5e-4,

        # Magnet inductance [H]
        'L' : 0.108
    },

    'B_50': 
    {
        # Operating current [A]
        'Iop' : 280,

        # Operating field [T]
        'B' : 6.24,

        # Operating SC temperature [K]
        'Top' : 4.2,

        # Critical temperature [K]
        'Tc' : 9.2,

        # Current-sharing temperature [K]
        'Tcs' : 5.50,

        # Residual resistivity ratio
        'RRR' : 50,

        # Cu/Nb-Ti ratio
        'ratio_cu_sc' : 0.9,

        # Total conductor diameter [m]
        'd_cond' : 8.5e-4,

        # Magnet inductance [H]
        'L' : 0.096
    },

    'B_100': 
    {
        # Operating current [A]
        'Iop' : 280,

        # Operating field [T]
        'B' : 6.24,

        # Operating SC temperature [K]
        'Top' : 4.2,

        # Critical temperature [K]
        'Tc' : 9.2,

        # Current-sharing temperature [K]
        'Tcs' : 5.50,

        # Residual resistivity ratio
        'RRR' : 100,

        # Cu/Nb-Ti ratio
        'ratio_cu_sc' : 0.9,

        # Total conductor diameter [m]
        'd_cond' : 8.5e-4,

        # Magnet inductance [H]
        'L' : 0.096
    }
}

# Maximum voltage across dump resistor [V]
Vmax = 600

figure_size = [9.6, 7.2]

if __name__ == "__main__":
  
    print('\n\n *** Protection results ***\n')

    t_switch_list = [0, 0.025, 0.05, 0.075, 0.1, 0.125, 0.15, 0.175, 0.2]
    t_switch_list = [0, 0.05, 0.1, 0.15, 0.2, 0.25]

    _plt.figure(figsize=figure_size)
    #_plt.rcParams.update({'font.size': 16})

    for model in dict_high_field_parameters:

        miits = []

        wire = _materials.SCWire(dict_high_field_parameters[model])

        R = _quench.calc_resistor(dict_high_field_parameters[model]['Iop'], Vmax)
        tau = dict_high_field_parameters[model]['L']/R

        for t_switch in t_switch_list:
            miits.append(
                _quench.calc_hot_spot(
                    wire.s_cu,
                    wire.s_sc,
                    dict_high_field_parameters[model]['Iop'],
                    tau,
                    t_switch,
                    dict_high_field_parameters[model]['RRR']
                )
            )


        print(' Results for Model {}\n'.format(model))
        print('    R = {} ohm'.format(R))
        print('    tau = {}'.format(tau))

   
        _plt.plot(t_switch_list, miits, '--x')

    #_plt.plot([t_switch_list[0], t_switch_list[-1]], [100, 100], 'k--')

    # _plt.title(
    #         'Hot-spot estimate @ Iop = {} A, RRR = {}, L = {:.3f} H, R_dump = {:.2f} ohm'.format(
    #             dict_high_field_parameters[model]['Iop'],
    #             dict_high_field_parameters[model]['RRR'],
    #             dict_high_field_parameters[model]['L'],
    #             R)
    #     )
    # _plt.title(
    #         'Comparison of hot-spot estimates @ Vmax = 600 V'
    #     )
        _plt.title('Comparison of hot-spot temperature estimates between model A and B')
    _plt.xlabel('t_prot [s]')
    _plt.ylabel('T_max [K]')
    _plt.legend(['Model A, RRR = 50', 'Model A, RRR = 100', 'Model B, RRR = 50','Model B, RRR = 100'])
    _plt.minorticks_on()
    _plt.grid(which='both', axis='both')
    _plt.tight_layout()
    _plt.show()
