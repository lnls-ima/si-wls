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
Vmin = 550
Vop = 600
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

    # Calculate hot-spot by MIITS method

    print('\n\n *** Protection results ***\n')

    t_switch_list = [0, 0.025, 0.05, 0.075, 0.1, 0.125, 0.15, 0.175, 0.2]
    #ratio_list = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2]

    hotspot_Imin_Vmin = []
    hotspot_Imax_Vmin = []
    hotspot_Imin_Vop = []
    hotspot_Imax_Vop = []
    hotspot_Imin_Vmax = []
    hotspot_Imax_Vmax = []

    # wire object created only to get areas
    wire = _materials.SCWire(dict_high_field_parameters)

    # update RRR to match model 8's for MIITS calulation
    dict_high_field_parameters['RRR'] = 25

    R1 = _quench.calc_resistor(I_max, Vop)
    tau1 = L/R1
    R2 = _quench.calc_resistor(I_max, Vmax)
    tau2 = L/R2
    R3 = _quench.calc_resistor(I_max, Vmin)
    tau3 = L/R3
    for t_switch in t_switch_list:
        hotspot_Imin_Vop.append(
            _quench.calc_hot_spot(
                wire.s_cu,
                wire.s_sc,
                I_min,
                tau1,
                t_switch,
                dict_high_field_parameters['RRR']
            )
        )
        hotspot_Imax_Vop.append(
            _quench.calc_hot_spot(
                wire.s_cu,
                wire.s_sc,
                I_max,
                tau1,
                t_switch,
                dict_high_field_parameters['RRR']
            )
        )
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
        hotspot_Imin_Vmin.append(
            _quench.calc_hot_spot(
                wire.s_cu,
                wire.s_sc,
                I_min,
                tau3,
                t_switch,
                dict_high_field_parameters['RRR']
            )
        )
        hotspot_Imax_Vmin.append(
            _quench.calc_hot_spot(
                wire.s_cu,
                wire.s_sc,
                I_max,
                tau3,
                t_switch,
                dict_high_field_parameters['RRR']
            )
        )

    print(' Results for Model 8\n')
    print('    R = {} ohm'.format(R1))
    print('    tau = {}'.format(tau1))
    print('    R2 = {} ohm'.format(R2))
    print('    tau2 = {}'.format(tau2))
    print('    R3 = {} ohm'.format(R3))
    print('    tau3 = {}'.format(tau3))

    _plt.figure(figsize=figure_size)
    _plt.plot(t_switch_list, hotspot_Imin_Vop, '--x')
    _plt.plot(t_switch_list, hotspot_Imax_Vop, '--x')
    _plt.plot(t_switch_list, hotspot_Imin_Vmax, '--x')
    _plt.plot(t_switch_list, hotspot_Imax_Vmax, '--x')
    _plt.plot(t_switch_list, hotspot_Imin_Vmin, '--x')
    _plt.plot(t_switch_list, hotspot_Imax_Vmin, '--x')

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
            '{} A, {:.2f} Ohm, {} V'.format(I_max, R2, I_max*R2),
            '{} A, {:.2f} Ohm, {} V'.format(I_min, R3, I_min*R3),
            '{} A, {:.2f} Ohm, {} V'.format(I_max, R3, I_max*R3)
            ]
    )

    _plt.xlabel('t_prot [s]')
    _plt.ylabel('T_max [K]')
    _plt.minorticks_on()
    _plt.grid(which='both', axis='both')
    _plt.show()

    # Calculate hot-spot by Wilson's method

    model8_RRR = 80
    time_step = 0.001 # sec
    curr_tol = 1 # A
    ps_delay = 0.07 # sec
    max_ps_voltage = 10 # V
    V_fw_diode = 10 # V
    L_I = {
        0.0 : 0.37428008998875145,
        1.0 : 0.37090854893138364,
        5.0 : 0.35742238470191234,
        10.0 : 0.3405646794150732,
        20.790378006872857: 0.3041844769403825,
        23.024054982817873: 296.65354330708664e-3,
        29.037800687285227: 276.37795275590554e-3,
        34.36426116838491: 257.8740157480314e-3,
        40.54982817869417: 236.2204724409449e-3,
        46.048109965635746: 217.5196850393701e-3,
        50.51546391752578: 209.25196850393704e-3,
        63.23024054982818: 186.02362204724412e-3,
        68.72852233676977: 176.18110236220477e-3,
        73.8831615120275: 171.0629921259843e-3,
        82.47422680412372: 162.59842519685043e-3,
        91.23711340206187: 154.13385826771656e-3,
        104.1237113402062: 147.83464566929138e-3,
        114.26116838487971: 142.7165354330709e-3,
        125.08591065292097: 139.3700787401575e-3,
        140.89347079037802: 134.6456692913386e-3,
        155.32646048109967: 131.2992125984252e-3,
        170.10309278350516: 128.74015748031502e-3,
        189.00343642611685: 125.98425196850397e-3,
        209.27835051546393: 123.62204724409457e-3,
        227.66323024054984: 122.04724409448824e-3,
    }

    hotspot_Imin_Vop = []
    hotspot_Imax_Vop = []
    hotspot_Imin_Vmax = []
    hotspot_Imax_Vmax = []
    hotspot_Imin_Vmin = []
    hotspot_Imax_Vmin = []

    for t_switch in t_switch_list:
        [
            R, I, Vq, Ve, Vc, Vl, Vnz, Eq, Eps, Tmax, Tavg,
            final_zone_transv_radius, final_zone_long_radius,
            time_axis, iter_cnt
        ] = _quench.simple_quench_propagation(
                I_op=I_min,
                T_cs=dict_high_field_parameters['Tcs'],
                T_op=dict_high_field_parameters['Top'],
                copper_area=wire.s_cu,
                nbti_area=wire.s_sc,
                insulator_area=0,
                inductanceI=L_I,
                magnet_vol=564 * (wire.s_cu + wire.s_sc),
                t_valid=t_switch,
                t_act=0,
                det_tresh=0,
                R_dump=R1,
                time_step=time_step,
                RRR=model8_RRR,
                B=dict_high_field_parameters['B'],
                alpha=0.01,
                tolerance=curr_tol,
                geometry='line',
                V_ps_max = max_ps_voltage,
                t_ps=ps_delay,
                V_fw_diode=V_fw_diode,
                use_magnetoresist=True,
                print_results=False
            )
        hotspot_Imin_Vop.append(Tmax[-1])

        [
            R, I, Vq, Ve, Vc, Vl, Vnz, Eq, Eps, Tmax, Tavg,
            final_zone_transv_radius, final_zone_long_radius,
            time_axis, iter_cnt
        ] = _quench.simple_quench_propagation(
                I_op=I_max,
                T_cs=dict_high_field_parameters['Tcs'],
                T_op=dict_high_field_parameters['Top'],
                copper_area=wire.s_cu,
                nbti_area=wire.s_sc,
                insulator_area=0,
                inductanceI=L_I,
                magnet_vol=564 * (wire.s_cu + wire.s_sc),
                t_valid=t_switch,
                t_act=0,
                det_tresh=0,
                R_dump=R1,
                time_step=time_step,
                RRR=model8_RRR,
                B=dict_high_field_parameters['B'],
                alpha=0.01,
                tolerance=curr_tol,
                geometry='line',
                V_ps_max = max_ps_voltage,
                t_ps=ps_delay,
                V_fw_diode=V_fw_diode,
                use_magnetoresist=True,
                print_results=False
            )
        hotspot_Imax_Vop.append(Tmax[-1])

        [
            R, I, Vq, Ve, Vc, Vl, Vnz, Eq, Eps, Tmax, Tavg,
            final_zone_transv_radius, final_zone_long_radius,
            time_axis, iter_cnt
        ] = _quench.simple_quench_propagation(
                I_op=I_min,
                T_cs=dict_high_field_parameters['Tcs'],
                T_op=dict_high_field_parameters['Top'],
                copper_area=wire.s_cu,
                nbti_area=wire.s_sc,
                insulator_area=0,
                inductanceI=L_I,
                magnet_vol=564 * (wire.s_cu + wire.s_sc),
                t_valid=t_switch,
                t_act=0,
                det_tresh=0,
                R_dump=R2,
                time_step=time_step,
                RRR=model8_RRR,
                B=dict_high_field_parameters['B'],
                alpha=0.01,
                tolerance=curr_tol,
                geometry='line',
                V_ps_max = max_ps_voltage,
                t_ps=ps_delay,
                V_fw_diode=V_fw_diode,
                use_magnetoresist=True,
                print_results=False
            )
        hotspot_Imin_Vmax.append(Tmax[-1])

        [
            R, I, Vq, Ve, Vc, Vl, Vnz, Eq, Eps, Tmax, Tavg,
            final_zone_transv_radius, final_zone_long_radius,
            time_axis, iter_cnt
        ] = _quench.simple_quench_propagation(
                I_op=I_max,
                T_cs=dict_high_field_parameters['Tcs'],
                T_op=dict_high_field_parameters['Top'],
                copper_area=wire.s_cu,
                nbti_area=wire.s_sc,
                insulator_area=0,
                inductanceI=L_I,
                magnet_vol=564 * (wire.s_cu + wire.s_sc),
                t_valid=t_switch,
                t_act=0,
                det_tresh=0,
                R_dump=R2,
                time_step=time_step,
                RRR=model8_RRR,
                B=dict_high_field_parameters['B'],
                alpha=0.01,
                tolerance=curr_tol,
                geometry='line',
                V_ps_max = max_ps_voltage,
                t_ps=ps_delay,
                V_fw_diode=V_fw_diode,
                use_magnetoresist=True,
                print_results=False
            )
        hotspot_Imax_Vmax.append(Tmax[-1])

        [
            R, I, Vq, Ve, Vc, Vl, Vnz, Eq, Eps, Tmax, Tavg,
            final_zone_transv_radius, final_zone_long_radius,
            time_axis, iter_cnt
        ] = _quench.simple_quench_propagation(
                I_op=I_min,
                T_cs=dict_high_field_parameters['Tcs'],
                T_op=dict_high_field_parameters['Top'],
                copper_area=wire.s_cu,
                nbti_area=wire.s_sc,
                insulator_area=0,
                inductanceI=L_I,
                magnet_vol=564 * (wire.s_cu + wire.s_sc),
                t_valid=t_switch,
                t_act=0,
                det_tresh=0,
                R_dump=R3,
                time_step=time_step,
                RRR=model8_RRR,
                B=dict_high_field_parameters['B'],
                alpha=0.01,
                tolerance=curr_tol,
                geometry='line',
                V_ps_max = max_ps_voltage,
                t_ps=ps_delay,
                V_fw_diode=V_fw_diode,
                use_magnetoresist=True,
                print_results=False
            )
        hotspot_Imin_Vmin.append(Tmax[-1])

        [
            R, I, Vq, Ve, Vc, Vl, Vnz, Eq, Eps, Tmax, Tavg,
            final_zone_transv_radius, final_zone_long_radius,
            time_axis, iter_cnt
        ] = _quench.simple_quench_propagation(
                I_op=I_max,
                T_cs=dict_high_field_parameters['Tcs'],
                T_op=dict_high_field_parameters['Top'],
                copper_area=wire.s_cu,
                nbti_area=wire.s_sc,
                insulator_area=0,
                inductanceI=L_I,
                magnet_vol=564 * (wire.s_cu + wire.s_sc),
                t_valid=t_switch,
                t_act=0,
                det_tresh=0,
                R_dump=R3,
                time_step=time_step,
                RRR=model8_RRR,
                B=dict_high_field_parameters['B'],
                alpha=0.01,
                tolerance=curr_tol,
                geometry='line',
                V_ps_max = max_ps_voltage,
                t_ps=ps_delay,
                V_fw_diode=V_fw_diode,
                use_magnetoresist=True,
                print_results=False
            )
        hotspot_Imax_Vmin.append(Tmax[-1])

    _plt.figure(figsize=figure_size)
    _plt.plot(t_switch_list, hotspot_Imin_Vop, '--x')
    _plt.plot(t_switch_list, hotspot_Imax_Vop, '--x')
    _plt.plot(t_switch_list, hotspot_Imin_Vmax, '--x')
    _plt.plot(t_switch_list, hotspot_Imax_Vmax, '--x')
    _plt.plot(t_switch_list, hotspot_Imin_Vmin, '--x')
    _plt.plot(t_switch_list, hotspot_Imax_Vmin, '--x')
    _plt.title(
            (
                "Hot-spot estimate by Winson's method"
                " @ Iop = {}/{} A, RRR = {}, B = {:.3f} T, variable L(I)"
                ).format(
                    I_min,
                    I_max,
                    model8_RRR,
                    dict_high_field_parameters['B']
                    )
        )
    _plt.legend(
        [
            '{} A, {:.2f} Ohm, {} V'.format(I_min, R1, I_min*R1),
            '{} A, {:.2f} Ohm, {} V'.format(I_max, R1, I_max*R1),
            '{} A, {:.2f} Ohm, {} V'.format(I_min, R2, I_min*R2),
            '{} A, {:.2f} Ohm, {} V'.format(I_max, R2, I_max*R2),
            '{} A, {:.2f} Ohm, {} V'.format(I_min, R3, I_min*R3),
            '{} A, {:.2f} Ohm, {} V'.format(I_max, R3, I_max*R3)
            ]
    )

    _plt.xlabel('t_prot [s]')
    _plt.ylabel('T_max [K]')
    _plt.minorticks_on()
    _plt.grid(which='both', axis='both')
    _plt.show()
