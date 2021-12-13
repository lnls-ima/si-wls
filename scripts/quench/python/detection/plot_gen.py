import sys as _sys
import traceback as _traceback
import numpy as _np
from matplotlib import pyplot as _plt
import materials as _materials
import detection as _detection

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

def nbti_specific_heat_estimation():
    # Ref.: M. McAshan, "MIITS Integrals for Copper and for Nb-46Ti
    up = 10
    low = 0
    step = 0.1
    T = _np.arange(low,up+step,step)
    Cp0 = _np.multiply(1.61e-4, T)
    Cp1 = _np.add(_np.multiply(1.61e-4, T), _np.multiply(2.711e-6, _np.power(T, 3)))
    Cp2 = _np.multiply(1.228e-5, _np.power(T, 3))
    # Plot results
    _plt.plot(T, _np.multiply(Cp0, 1e3))
    _plt.plot(T, _np.multiply(Cp1, 1e3))
    _plt.plot(T, _np.multiply(Cp2, 1e3))
    _plt.legend(['Cp0', 'Cp1', 'Cp2'])
    _plt.xlabel('Temperature [K]', fontsize=14)
    _plt.ylabel('Nb-Ti specific heat [J/kg.K]', fontsize=14)
    _plt.title('Ref.: M. McAshan, "MIITS Integrals for Copper and for Nb-46Ti" ')
    _plt.grid(True)
    _plt.show()

def prop_velocity_estimations():
    # Operation parameters
    ## Operating current [A]
    Iop = 250
    ## Operating SC temperature [K]
    Top = 4.2
    ## Critical temperature [K]
    Tc = 9.2
    ## Current-sharing temperature [K]
    Tcs = 5.95
    # Transition temperature [k]
    Tjoule = _np.divide(_np.add(Tc, Tcs), 2)
    # Wire parameters
    ## Residual resistivity ratio
    RRR = 50
    # Cu/Nb-Ti ratio
    ratio_cu_sc = [0.6, 0.8, 1, 1.2]
    ## Total conductor diameter [mm]
    d_cond = 0.82
    # Total conductor and composite areas [mm²]
    s_cond = _np.multiply(_np.pi, _np.power(_np.divide(d_cond, 2), 2))
    [s_sc, s_cu] = _materials.calc_area_sc_cu(d_cond, ratio_cu_sc)
    # Materials properties
    # Copper @ RRR = 100, Tjoule = 5 K
    # Refs.: 
    #   - https://www.copper.org/resources/properties/cryogenic/
    #   - KN5010 Nº4 (Davide)
    #   - M. McAshan, "MIITS Integrals for Copper and for Nb-46Ti"
    # Copper fraction
    f_cu = _np.divide(s_cu, s_cond)
    # Resistivity [Ohm.m]
    resty_cu = _materials.copper_resistivity(Tjoule, RRR)
    # Density [kg/m³]
    dsty_cu = 9000
    # Specific heat [J/kg.K]
    c_cu = 0.2
    # Thermal conductivity [W/m.K]
    k_cu = 400
    # Nb-Ti @ Tjoule
    ## NbTi fraction
    f_sc = _np.divide(s_sc, s_cond)
    resty_sc = 1e-5
    dsty_sc = 6500
    ## Estimated density from 50-50% NbTi alloy [km/m³]
    c_sc = _np.multiply(0.07, Tjoule)
    ## Estimated from M. McAshan, "MIITS Integrals for Copper and for Nb-46Ti"
    c_sc = 1.5
    #c_sc = 10000
    ## Ref.: "Thermal Conductivity and Electrical Resistivity of NbTi Alloys at Low Temperatures"
    k_sc = 0.5
    #
    # Current density. During quench, all current goes to copper.
    Jop = _np.divide(_np.multiply(Iop, 1e6), s_cu)
    # Composite volumetric specific heat
    C_comp = _np.add(
        _np.multiply(_np.multiply(f_cu, dsty_cu), c_cu),
        _np.multiply(_np.multiply(f_sc, dsty_sc), c_sc)
        )
    #C_comp = dsty_cu*c_cu;
    # Composite resistivity
    resty_comp = _np.divide(
        1,
        _np.add(
            _np.divide(f_cu, resty_cu),
            _np.divide(f_sc, resty_sc)
            )
        )
    # Composite thermal conductivity
    k_comp = _np.add(_np.multiply(f_cu, k_cu), _np.multiply(f_sc, k_sc))
    # Velocity estimation
    method = 'adiabatic'
    vqs = _detection.calc_prop_velocity(Jop, C_comp, resty_comp, k_comp, Tjoule, Top, method)
    # Plot results
    #plot(ratio_cu_sc, vqs,'d:','MarkerSize',15)
    _plt.plot(ratio_cu_sc, vqs, linestyle='dotted', markersize=15)
    _plt.title('Estimated propagation velocity @ Iop = 250 A, Top = 4.2 K, Tc = 9.8 K, Tcs = 5.9K')
    _plt.xlabel('Ratio Cu/Nb-Ti', fontsize=14)
    _plt.ylabel('Propagtion velocity [m/s]', fontsize=14)
    _plt.legend(['200', '100', '50'], title='RRR')
    _plt.grid(True)
    _plt.show()
