import sys as _sys
import traceback as _traceback
import numpy as _np
from matplotlib import pyplot as _plt

def calc_v_correction_factor():
    try:
        step = 0.001
        up = 0.999
        low = -10
        y = _np.arange(low,up+step,step)
        b = _np.divide(
                _np.subtract(
                    1,
                    _np.multiply(2,y)
                ),
                _np.sqrt(_np.subtract(1,y))
            )
        _plt.plot(y,b)
        _plt.grid(True)
        _plt.show()
        return b
    except Exception:
        _traceback.print_exc(file=_sys.stdout)

def compare_ratio_vs_iso_sc_area():
    # Total diameter [mm]
    d_total = 1.05
    # Isolation thickness [um]
    up = 150
    low = 100
    step = 10
    iso = _np.arange(low,up+step,step)
    # Superconductor area [mm²] 	
    up = 0.25
    low = 0.2
    step = 0.01
    s_sc = _np.arange(low,up+step,step)
    # Conductors diameter
    d_cond = _np.zeros((len(iso), len(s_sc)))
    # Ratios Cu/Nb-Ti
    ratios = _np.zeros((len(iso),len(s_sc)))

    # Iterate for isolations ans SC areas
    for i in range(0, len(iso)):
        for s in range(0, len(s_sc)):
            d_cond = _np.subtract(d_total, 0.002*iso[i])
            ratios[i,s] = calc_ratio_cu_sc(d_cond, s_sc[s])
        _plt.plot(s_sc, ratios[i,:])
    # Plot results
    legend_labels = [str(i) for i in iso]
    _plt.legend(legend_labels, title='Isolation [um]')
    _plt.xlabel('Nb-Ti area [mm2]')
    _plt.ylabel('Ratio Cu/Nb-Ti')
    _plt.title('Ratio Cu/Nb-Ti Vs Isolation thickness and Nb-Ti area')
    _plt.grid(True)
    _plt.show()
