import matplotlib.pyplot as _plt
import numpy as _np
import sys as _sys
import traceback as _traceback

import materials as _materials

def calc_detection_voltage(vq,rho,tqd,Io,Acu):
    try:
        if type(vq) == _np.ndarray:
            vdets = []
            for v in vq:
                R = _np.multiply(_np.multiply(v, tqd), _np.divide(rho, Acu))
                vdet = _np.multiply(R, Io)
                vdets.append(vdet)
            vdets = _np.array(vdets)
            return vdets

        else:
            R = _np.multiply(_np.multiply(vq, tqd), _np.divide(rho, Acu))
            return _np.multiply(R, Io)
    except Exception:
        _traceback.print_exc(file=_sys.stdout)

def calc_prop_velocity(Jo, C, rho, k, Tjoule, Top, method):
    try:
        v = _np.multiply(
                _np.divide(Jo,C),
                _np.sqrt(
                    _np.divide(
                        _np.multiply(rho,k),
                        _np.subtract(Tjoule,Top)
                    )
                )
            )
        if method == "adiabatic":
            prop_vel = v
        elif method == "cooled":
            corr_factor = 0.0
            prop_vel = _np.multiply(corr_factor, v)
        else:
            prop_vel = 5
        return prop_vel
    except Exception:
        _traceback.print_exc(file=_sys.stdout)

def calc_detection_time(vq,rho,vdet,Io,Acu):
    """ Inverse of detection voltage calculation
    """
    try:
        return _np.multiply(
            _np.divide(vdet, Io), _np.divide(_np.divide(Acu, rho), vq)
            )
    except Exception:
        _traceback.print_exc(file=_sys.stdout)
