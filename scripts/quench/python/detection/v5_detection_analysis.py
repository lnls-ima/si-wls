#!/usr/bin/env python

import detection as _detection
import materials as _materials
import plot_gen as _plot_gen

import numpy as _np
import matplotlib.pyplot as _plt

### Operation parameters for high-field
dict_high_field_parameters = {

    # Operating current [A]
    'Iop' : 275,

    # Operating field [T]
    'B' : [0,6],

    # Operating SC temperature [K]
    'Top' : 4.2,

    # Critical temperature [K]
    'Tc' : 9.2,

    # Current-sharing temperature [K]
    'Tcs' : 6.06,

    # Residual resistivity ratio
    'RRR' : 100,

    # Cu/Nb-Ti ratio
    'ratio_cu_sc' : 0.9,

    # Total conductor diameter [mm]
    'd_cond' : 0.85
}
    
if __name__ == "__main__":
    
    # list_Top = [4.2,5]
    # list_RRR = [50, 100, 200]

    # for t_op in list_Top:
    #     for rrr in list_RRR:
    #         dict_high_field_parameters['Top'] = t_op
    #         dict_high_field_parameters['RRR'] = rrr

    vqs = _detection.prop_velocity_estimations(dict_high_field_parameters)
