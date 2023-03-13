import sys as _sys
import traceback as _traceback
import numpy as _np
from matplotlib import pyplot as _plt
import detection as _detection
import materials as _materials
import quench as _quench

"""
Resistor matrix with n_parallel lines and n_series columns,
grounded at the middle.

         __/\/\/\/\/\___/\/\/\/\/\_ ..._ _..._/\/\/\/\/\___/\/\/\/\/\_
         |            |                 |                |            |
        ...          ...               ...              ...          ...
         |            |                 |                |            |
(+) ______/\/\/\/\/\__|_/\/\/\/\/\_ ..._|_..._/\/\/\/\/\_|_/\/\/\/\/\_|_______ (-)
         |            |                 |                |            |
        ...          ...               ...              ...          ...
         |            |                 |                |            |
         |_/\/\/\/\/\_|_/\/\/\/\/\_ ..._ _..._/\/\/\/\/\_|_/\/\/\/\/\_|
                                        |
                                      _____
                                       ___
                                        _
"""
class ResistorBank:
    def __init__(self, n_parallel=1, n_series=1, r_eq=1):
        if n_parallel< 1 or n_series < 1:
            raise ValueError('Resistor matrix cannot be smaller than (1, 1)')
        self.r_unit = self.get_unit_resistance(r_eq, n_parallel, n_series)
        self.r_matrix = _np.ones((n_parallel, n_series)) * self.r_unit
        self.n_parallel = n_parallel
        self.n_series = n_series
        return
    
    def short_failure(self, positions, per=100):
        if not isinstance(positions, list):
            positions = [positions]
        for l, c in positions:
            if (
                l >= self.n_parallel
                or c >= self.n_series
                ):
                raise ValueError(
                    'Resistor position out of matrix range'
                    )
            if per > 100 or per < 0:
                raise ValueError(
                    'Failure percentage must be within 0 and 100 %'
                    )
            self.r_matrix[l, c] *= (100 - per)/100

    def open_failure(self, positions):
        if not isinstance(positions, list):
            positions = [positions]
        for l, c in positions:
            if (
                l >= self.n_parallel
                and c >= self.n_series
                ):
                raise ValueError(
                    'Resistor position out of matrix range'
                    )
            self.r_matrix[l, c] = _np.inf

    def get_equivalent_resistance(self):
        eq_r = 0
        r_matrix_transp = _np.transpose(self.r_matrix)
        for c in r_matrix_transp:
            inv_paralel_r = 0
            for r in c:
                if r == 0:
                    inv_paralel_r = _np.inf
                    break
                else:
                    inv_paralel_r += _np.divide(1, r)
            eq_r += _np.divide(1, inv_paralel_r)
        return eq_r
    
    def get_equivalent_left_resistance(self):
        eq_r = 0
        r_matrix_transp = _np.transpose(self.r_matrix)
        for c in r_matrix_transp[0:int(_np.floor(self.n_series/2))]:
            inv_paralel_r = 0
            for r in c:
                if r == 0:
                    inv_paralel_r = _np.inf
                    break
                else:
                    inv_paralel_r += _np.divide(1, r)
            eq_r += _np.divide(1, inv_paralel_r)
        return eq_r

    def get_equivalent_right_resistance(self):
        eq_r = 0
        r_matrix_transp = _np.transpose(self.r_matrix)
        for c in r_matrix_transp[int(_np.floor(self.n_series/2)):]:
            inv_paralel_r = 0
            for r in c:
                if r == 0:
                    inv_paralel_r = _np.inf
                    break
                else:
                    inv_paralel_r += _np.divide(1, r)
            eq_r += _np.divide(1, inv_paralel_r)
        return eq_r

    def get_unit_resistance(self, r_eq, n_parallel, n_series):
        return (_np.divide(r_eq, n_series)) * n_parallel
