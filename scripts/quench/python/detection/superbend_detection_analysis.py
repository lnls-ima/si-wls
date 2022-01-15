#!/usr/bin/env python

import detection as _detection
import materials as _materials
import plot_gen as _plot_gen

import numpy as _np
import matplotlib.pyplot as _plt

### Operation parameters for high-field
dict_high_field_parameters = {

    # Operating current [A]
    'Iop' : 128,

    # Operating field [T]
    'B' : 6,

    # Operating SC temperature [K]
    'Top' : 4.2,

    # Critical temperature [K]
    'Tc' : 9.2,

    # Current-sharing temperature [K]
    'Tcs' : 6,

    # Residual resistivity ratio
    'RRR' : 50,

    # Cu/Nb-Ti ratio
    'ratio_cu_sc' : 1.4,

    # Total conductor diameter [mm]
    'd_cond' : 0.8
}
    
def calc_detection_voltage(vq,rho,tqd,Io,Acu):
    try:
        R = _np.multiply(_np.multiply(vq, tqd), _np.divide(rho, Acu))
        return _np.multiply(R, Io)
    except Exception:
        _traceback.print_exc(file=_sys.stdout)

if __name__ == "__main__":
    
    # list_Top = [4.2,5]
    # list_RRR = [50, 100, 200]

    # for t_op in list_Top:
    #     for rrr in list_RRR:
    #         dict_high_field_parameters['Top'] = t_op
    #         dict_high_field_parameters['RRR'] = rrr

    vqs = _detection.prop_velocity_estimations(dict_high_field_parameters)

    print('\n ### Propagation velocity estimations')
    print('\n    Propagation velocity = {} m/s\n\n'.format(vqs))
    
    # Plot results
    _plt.plot([2.414, 3.85, 5.391], vqs, 'd:')
    #_plt.plot(2.414, vqs, 'd:')

    _plt.title(
        'Estimated propagation velocity @ Iop = {} A, Top = {} K, RRR = {}, Ratio Cu/Nb-Ti = {}'.format(
            dict_high_field_parameters['Iop'],
            dict_high_field_parameters['Top'],
            dict_high_field_parameters['RRR'],
            dict_high_field_parameters['ratio_cu_sc']
            )
    )

    _plt.xlabel('Nb-Ti specific heat [J/kg.K]', fontsize=14)
    _plt.ylabel('Propagtion velocity [m/s]', fontsize=14)
    _plt.grid(visible=True, which='both')
    _plt.show()