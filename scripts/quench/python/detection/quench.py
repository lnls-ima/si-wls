import sys as _sys
import traceback as _traceback
import numpy as _np
from matplotlib import pyplot as _plt
import detection as _detection
import materials as _materials

CU_PROPERTIES = _materials.Copper()
NBTI_PROPERTIES = _materials.NbTi()

MIITS_table = {
    'Cu': {
        25: {
            'T':
            _np.array(
                [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400, 420, 440, 460, 480, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000, 1050, 1100, 1150, 1200, 1250, 1300]
            ),
            'MIITS':
            _np.array(
                [0.3482, 4.999, 27.22, 76.39, 147, 223.8, 297.9, 366.6, 429.3, 486.3, 586.1, 671.2, 745.6, 811.7, 871.1, 925, 974.5, 1020, 1063, 1102, 1140, 1175, 1208, 1240, 1270, 1299, 1327, 1354, 1379, 1404, 1461, 1514, 1563, 1609, 1652, 1693, 1732, 1768, 1804, 1838, 1870, 1902, 1932, 1962, 1990, 2018]
            )
        },
        50: {
            'T':
            _np.array(
                [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400, 420, 440, 460, 480, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000, 1050, 1100, 1150, 1200, 1250, 1300]
            ),
            'MIITS':
            _np.array(
                [0.6964, 9.9110, 51.7800, 134.1000, 236.8000, 336.2000, 425.1000, 503.7000, 573.3000, 635.4000, 742.0000, 831.5000, 909.0000, 977.4000, 1039.0000, 1094, 1145, 1191, 1235, 1275, 1313, 1349, 1383, 1415, 1445, 1475, 1503, 1530, 1556, 1580, 1639, 1692, 1742, 1788, 1831, 1872, 1911, 1948, 1983, 2018, 2051, 2082, 2113, 2142, 2171, 2199]
            )
        },
        100: {
            'T':
            _np.array(
                [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400, 420, 440, 460, 480, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000, 1050, 1100, 1150, 1200, 1250, 1300]
            ),
            'MIITS':
            _np.array(
                [1.3930, 19.4900, 94.7100, 219.7000, 352.7000, 469.4000, 568.2000, 653.0000, 726.7000, 791.7000, 902.0000, 993.9000, 1073.0000, 1143.0000, 1205.0000, 1261, 1312, 1359, 1403, 1444, 1482, 1518, 1552, 1585, 1616, 1645, 1673, 1700, 1726, 1751, 1810, 1863, 1913, 1960, 2003, 2044, 2083, 2120, 2156, 2190, 2223, 2255, 2286, 2315, 2344, 2372]
            )
        }
    },
    'Nb-Ti': {
        25: {
            'T':
            _np.array(
                [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400, 420, 440, 460, 480, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000, 1050, 1100, 1150, 1200, 1250, 1300]
            ),
            'MIITS':
            _np.array(
                [1.591, 14.89, 60.04, 142.9, 242.6, 338.5, 422.5, 494.4, 556.1, 609.9, 699.8, 773.1, 835.3, 889.3, 937.3, 980.4, 1020, 1056, 1089, 1120, 1150, 1177, 1203, 1228, 1251, 1274, 1295, 1316, 1336, 1355, 1400, 1441, 1479, 1515, 1549, 1581, 1611, 1639, 1667, 1693, 1718, 1742, 1765, 1787, 1808, 1829]
            )
        },
        50: {
            'T':
            _np.array(
                [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400, 420, 440, 460, 480, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000, 1050, 1100, 1150, 1200, 1250, 1300]
            ),
            'MIITS':
            _np.array(
                [3.1820, 29.5600, 114.7000, 253.9000, 399.0000, 523.1000, 624.0000, 706.3000, 774.9000, 833.5000, 929.5000, 1007.0000, 1071.0000, 1127.0000, 1177.0000, 1221, 1261, 1298, 1332, 1364, 1394, 1422, 1448, 1473, 1497, 1520, 1541, 1562, 1582, 1602, 1647, 1689, 1727, 1763, 1797, 1829, 1859, 1888, 1916, 1942, 1967, 1991, 2014, 2037, 2058, 2079]
            )
        },
        100: {
            'T':
            _np.array(
                [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400, 420, 440, 460, 480, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000, 1050, 1100, 1150, 1200, 1250, 1300]
            ),
            'MIITS':
            _np.array(
                [6.3630, 58.2300, 211.6000, 423.4000, 611.8000, 757.7000, 869.8000, 958.6000, 1031.0000, 1092.0000, 1192.0000, 1271.0000, 1337.0000, 1394.0000, 1444.0000, 1489, 1530, 1567, 1602, 1634, 1664, 1692, 1719, 1744, 1768, 1791, 1812, 1833, 1854, 1873, 1918, 1960, 1999, 2035, 2069, 2101, 2132, 2161, 2188, 2214, 2240, 2264, 2287, 2309, 2331, 2352]
            )
        }
    }
}

class QuenchZone:
    """ Class to hold quench zone parameters"""
    def __init__(self,
            long_radius=0,
            transv_radius=0,
            hole_long_radius=0,
            hole_transv_radius=0,
            T=0,
            rho=0,
            R=0
            ):
        self.long_radius = long_radius
        self.transv_radius = transv_radius
        self.hole_long_radius = hole_long_radius
        self.hole_transv_radius = hole_transv_radius
        self.T = T
        self.rho = rho
        self.R = R

def nbti_heat_capacity_below_9k(temp, B):
    return 0.0082*_np.power(temp,3) + 0.011*B*temp

def nbti_avg_heat_capacity_below_9K(T2, T1, B, num_steps=1000):
    # Definite integral of the C_nbti function
    x = _np.linspace(T1, T2, num=num_steps, endpoint=True)
    y = _np.array([NBTI_PROPERTIES.calc_specific_heat(T, B, True) for T in x])
    integral_val = _np.trapz(y, x)
    return integral_val / (T2 - T1)

def cu_avg_heat_capacity(T2, T1, num_steps=1000):
    x = _np.linspace(T1, T2, num=num_steps, endpoint=True)
    y = _np.array([CU_PROPERTIES.calc_specific_heat(T) for T in x])
    integral_val = _np.trapz(y, x)
    return integral_val / (T2 - T1)

def composite_vol_specific_heat_sc(copper_area, nbti_area, T_joule, T_op, B):
    # calculate average Cu heat capacity
    C_cu = cu_avg_heat_capacity(T_joule, T_op)
    # calculate average Nb-Ti heat capacity
    C_nbti = nbti_avg_heat_capacity_below_9K(T_joule, T_op, B)
    # return volumetric composite heat capacity
    cond_area = _np.add(nbti_area, copper_area)
    f_cu = _np.divide(copper_area, cond_area)
    f_nbti = _np.divide(nbti_area, cond_area)
    dsty_cu = CU_PROPERTIES.density
    dsty_nbti = NBTI_PROPERTIES.density
    return _np.add(
        _np.multiply(_np.multiply(f_cu, dsty_cu), C_cu),
        _np.multiply(_np.multiply(f_nbti, dsty_nbti), C_nbti)
        )

def composite_vol_specific_heat_nc(copper_area, nbti_area, temp, B):
    # calculate Cu heat capacity
    C_cu = CU_PROPERTIES.calc_specific_heat(temp)
    # calculate non-superconducting Nb-Ti heat capacity
    C_nbti = NBTI_PROPERTIES.calc_specific_heat(temp, B, False)
    # return composite heat capacity
    cond_area = _np.add(nbti_area, copper_area)
    f_cu = _np.divide(copper_area, cond_area)
    f_nbti = _np.divide(nbti_area, cond_area)
    dsty_cu = CU_PROPERTIES.density
    dsty_nbti = NBTI_PROPERTIES.density
    return _np.add(
        _np.multiply(_np.multiply(f_cu, dsty_cu), C_cu),
        _np.multiply(_np.multiply(f_nbti, dsty_nbti), C_nbti)
        )

def nbti_avg_thermal_conductivity(T2, T1, num_steps=1000):
    x = _np.linspace(T1, T2, num=num_steps, endpoint=True)
    y = _np.array([NBTI_PROPERTIES.calc_thermal_conductivity(T) for T in x])
    integral_val = _np.trapz(y, x)
    return integral_val / (T2 - T1)

def cu_avg_thermal_conductivity(T2, T1, RRR, num_steps=1000):
    x = _np.linspace(T1, T2, num=num_steps, endpoint=True)
    y = _np.array([CU_PROPERTIES.calc_thermal_conductivity(T, RRR) for T in x])
    integral_val = _np.trapz(y, x)
    return integral_val / (T2 - T1)

def composite_thermal_conductivity(copper_area, nbti_area, T2, T1, RRR):
    # avg Nb-Ti k
    k_nbti = nbti_avg_thermal_conductivity(T2, T1)
    # avg Cu k
    k_cu = cu_avg_thermal_conductivity(T2, T1, RRR)
    # composite result
    cond_area = _np.add(nbti_area, copper_area)
    f_cu = _np.divide(copper_area, cond_area)
    f_nbti = _np.divide(nbti_area, cond_area)
    return _np.add(
        _np.multiply(f_cu, k_cu), _np.multiply(f_nbti, k_nbti)
        )

def composite_resistivity(temp, copper_area, nbti_area, RRR, B, is_sc):
    rho_cu = CU_PROPERTIES.calc_resistivity(temp, RRR, B)
    rho_nbti = NBTI_PROPERTIES.calc_resistivity(temp, is_sc)    
    cond_area = _np.add(nbti_area, copper_area)
    f_cu = _np.divide(copper_area, cond_area)
    f_nbti = _np.divide(nbti_area, cond_area)
    return  _np.divide(
        _np.multiply(rho_cu, rho_nbti),
        _np.add(
            _np.multiply(rho_cu, f_nbti),
            _np.multiply(rho_nbti,f_cu)
            )
        )

def heating_factor(
        J, temp, copper_area, nbti_area, RRR, B):
    # composite resistivity
    rho_cu = CU_PROPERTIES.calc_resistivity(temp, RRR, B)
    rho_nbti = NBTI_PROPERTIES.calc_resistivity(temp, False)
    cond_area = _np.add(nbti_area, copper_area)
    f_cu = _np.divide(copper_area, cond_area)
    f_nbti = _np.divide(nbti_area, cond_area)
    rho = _np.divide(
        _np.multiply(rho_cu, rho_nbti),
        _np.add(
            _np.multiply(rho_cu, f_nbti),
            _np.multiply(rho_nbti, f_cu)
            )
        )
    # composite heat capacity
    c_avg = composite_vol_specific_heat_nc(copper_area, nbti_area, temp, B)
    # result heating
    return (_np.power(J, 2) * rho) / c_avg

def geometric_factor(
        transv_radius, long_radius,
        hole_transv_radius, hole_long_radius,
        copper_area, nbti_area, insulator_area, geometry='ellipsoid'):
    if geometry == 'ellipsoid':
        # calculate ellipsoid volume
        vol = ellipsoid_vol(long_radius, transv_radius)
        # calculate ellipsoid hole volume
        hole = ellipsoid_vol(hole_long_radius, hole_transv_radius)
        # subtract hole from volume
        vol = vol - hole
        # calculate copper to full conductor area ratio
        conductor_ratio = copper_area / (copper_area + nbti_area + insulator_area)
        # calculate volume corresponding to copper wire
        vol_copper = vol * conductor_ratio
        # find proportional length of copper wire in zone
        len_copper = vol_copper / copper_area
        # return (l_cu / A_cu) factor
        return len_copper / copper_area
    elif geometry == 'line':
        # consider propagation as one dimensional
        return 2*(long_radius - hole_long_radius) / copper_area 
    else:
        raise ValueError('Invalid geometry: {0}'.format(geometry))

def ellipsoid_vol(a, b):
    # calculate ellipsoid volume
    return 4/3 * _np.pi * _np.power(b, 2) * a

def simple_quench_propagation(
        I_op, T_cs, T_op, copper_area, nbti_area, insulator_area,
        inductance, magnet_vol, t_dump=0, R_dump=0, time_step=0.000001, RRR=100,
        B=0, alpha=0.03, tolerance=1e-6, geometry='ellipsoid'
        ):
    """
       Refs.: 
       [1] M. Wilson, "Lecture 4: Quenching and Protection", JUAS, February 2016. """
    # wire properties
    wire = _materials.SCWire(
        {
            'Iop': I_op,
            'B': B,
            'Top': T_op,
            'Tc': NBTI_PROPERTIES.Tc,
            'Tcs': T_cs,
            'RRR': RRR,
            'ratio_cu_sc': copper_area/nbti_area,
            'd_cond': 2*_np.sqrt(
                (copper_area+nbti_area+insulator_area)
                /_np.pi
                )
        }
    )
    T_joule = wire.Tjoule
    cond_area = _np.add(copper_area, nbti_area)
    # quench evolution output variables
    iter_cnt = 0
    zone_list = []
    I = []
    R = []
    Vq = []
    Vd = []
    Eq = []
    Tmax = []
    Tavg = []
    final_zone_transv_radius = []
    final_zone_long_radius = []
    # initial condition
    propagation_end = False
    E_quench = 0
    I.append(I_op)
    R.append(0)
    Vq.append(0)
    Vd.append(0)
    Eq.append(0)
    Tmax.append(T_op)
    Tavg.append(T_op)
    final_zone_long_radius.append(0)
    final_zone_transv_radius.append(0)
    # calculate initial composite resistivity
    rho_0 = wire.resty_comp
    # create initial zone
    zone_list.append(
        QuenchZone(
            long_radius=0, transv_radius=0,
            hole_long_radius=0, hole_transv_radius=0,
            T=T_joule, rho=rho_0, R=0
        )
    )
    # calculate initial current density
    J0 = I_op / cond_area
    # calculate average heat capacity
    C_avg = composite_vol_specific_heat_sc(
        copper_area, nbti_area, T_joule, T_op, B
    )
    # calculate avg thermal conductivity below 9 K
    k_avg = composite_thermal_conductivity(
        copper_area, nbti_area, T_joule, T_op, RRR
    )
    # calculate prop velocity
    vq = _detection.calc_prop_velocity(
        J0, C_avg, rho_0, k_avg, T_joule, T_op, 'adiabatic'
    )
    # grow zone based on vq
    zone_list[0].long_radius += vq * time_step
    zone_list[0].transv_radius += alpha * vq * time_step
    # calculate current density after quench
    J = J0
    # increase zone 1 temperature
    zone_list[0].T += time_step * heating_factor(
        J, zone_list[0].T, copper_area, nbti_area, RRR, B
        )
    # update zone 1 resistivity
    zone_list[0].rho = composite_resistivity(
        zone_list[0].T, copper_area, nbti_area, RRR, B, is_sc=False
        )
    # update resistance
    zone_list[0].R = zone_list[0].rho * geometric_factor(
        zone_list[0].transv_radius, zone_list[0].long_radius,
        0, 0, copper_area, nbti_area, insulator_area, geometry
        )
    R_quench = zone_list[0].R
    # update current and add dump resistance
    if (iter_cnt*time_step >= t_dump):
        R_total = R_quench + R_dump
        I_op = I_op - I_op*(R_total/inductance)*time_step
        V_quench = R_quench * I_op
        V_dump = R_dump * I_op
        E_quench += I_op * V_quench * time_step
    else:
        R_total = R_quench
        I_op = I_op
        V_quench = R_quench * I_op
        V_dump = 0
        E_quench += I_op * V_quench * time_step
    # update current density
    J = I_op / cond_area
    # update prop velocity
    vq = _detection.calc_prop_velocity(
        J, C_avg, rho_0, k_avg, T_joule, T_op, 'adiabatic'
    )
    # update outputs
    R.append(R_quench)
    I.append(I_op)
    Vq.append(V_quench)
    Vd.append(V_dump)
    Eq.append(E_quench)
    Tmax.append(zone_list[0].T)
    Tavg.append(zone_list[0].T)
    final_zone_transv_radius.append(zone_list[0].transv_radius)
    final_zone_long_radius.append(zone_list[0].long_radius)
    iter_cnt += 1
    # ITERATION LOOP
    while (I_op > tolerance):
        # DEBUG
        print('num iter = {0}'.format(iter_cnt))
        print('max temp = {0}'.format(zone_list[0].T))
        print('Iop = {0}'.format(I_op))
        print('\n')
        # add new outer zone
        if not propagation_end:
            # new zone size
            new_long_radius = (
                zone_list[-1].long_radius + vq*time_step
            )
            new_transv_radius = (
                zone_list[-1].transv_radius + alpha*vq*time_step
            )
            # stop propagation if whole magnet quenched
            if geometry == 'ellipsoid':
                if ellipsoid_vol(new_long_radius, new_transv_radius) >= magnet_vol:
                    propagation_end = True
            elif geometry == 'line':
                if (
                    2*new_long_radius
                    * (copper_area + nbti_area + insulator_area)
                     >= magnet_vol
                    ):
                    propagation_end = True
            else:
                raise ValueError('Invalid geometry: {0}'.format(geometry))    
            # new zone
            zone_list.append(
                QuenchZone(
                    long_radius=new_long_radius,
                    transv_radius=new_transv_radius,
                    hole_long_radius=zone_list[-1].long_radius,
                    hole_transv_radius=zone_list[-1].transv_radius,
                    T=T_joule, rho=rho_0, R=0 
                )
            )
        # Reset R quench for update
        R_quench = 0
        # update zones
        for zone in zone_list:
            # increase temperature
            zone.T += time_step * heating_factor(
                J, zone.T, copper_area, nbti_area, RRR, B
                )
            # update resistivity
            zone.rho = composite_resistivity(
                zone.T, copper_area, nbti_area, RRR, B, is_sc=False
                )
            # update resistance
            zone.R = zone.rho * geometric_factor(
                zone.transv_radius, zone.long_radius,
                zone.hole_transv_radius,
                zone.hole_long_radius,
                copper_area, nbti_area, insulator_area,
                geometry
                )
            # add to R quench
            R_quench += zone.R
        # update current and add dump resistance
        if (iter_cnt*time_step >= t_dump):
            R_total = R_quench + R_dump
            I_op = (
                I_op - I_op*(R_total/inductance)*time_step
            )
            V_quench = R_quench * I_op
            V_dump = R_dump * I_op
            E_quench += I_op * V_quench * time_step
        else:
            R_total = R_quench
            I_op = I_op
            V_quench = R_quench * I_op
            V_dump = 0
            E_quench += I_op * V_quench * time_step
        # update current density
        J = I_op / cond_area
        # update prop velocity
        vq = _detection.calc_prop_velocity(
            J, C_avg, rho_0, k_avg, T_joule, T_op, 'adiabatic'
        )
        # calculate average quench temperature
        for zone in zone_list:
            T_weighted_avg = _np.average(
                [zone.T for zone in zone_list],
                weights=[
                    (zone.long_radius - zone.hole_long_radius)
                    for zone in zone_list
                ]
            )
        # update outputs
        R.append(R_quench)
        I.append(I_op)
        Vq.append(V_quench)
        Vd.append(V_dump)
        Eq.append(E_quench)
        Tmax.append(zone_list[0].T)
        Tavg.append(T_weighted_avg)
        final_zone_transv_radius.append(zone_list[-1].transv_radius)
        final_zone_long_radius.append(zone_list[-1].long_radius)
        iter_cnt += 1
    # print results
    t_total = (len(R)-1) * time_step
    time_axis = _np.linspace(0, t_total, len(R))
    # R quench plot
    _plt.figure(figsize=[9.6, 7.2])
    _plt.plot(time_axis, R, '-x')
    _plt.title('Quench resistance growth')
    _plt.xlabel('Time [sec]', fontsize=14)
    _plt.ylabel('R [ohm]', fontsize=14)
    _plt.minorticks_on()
    _plt.grid(which='both', axis='both')
    # I plot
    _plt.figure(figsize=[9.6, 7.2])
    _plt.plot(time_axis, I, '-x')
    _plt.title('Current decay')
    _plt.xlabel('Time [sec]', fontsize=14)
    _plt.ylabel('I [A]', fontsize=14)
    _plt.minorticks_on()
    _plt.grid(which='both', axis='both')
    # Vq plot
    _plt.figure(figsize=[9.6, 7.2])
    _plt.plot(time_axis, Vq, '-x')
    _plt.title('Quench voltage')
    _plt.xlabel('Time [sec]', fontsize=14)
    _plt.ylabel('Voltage [V]', fontsize=14)
    _plt.minorticks_on()
    _plt.grid(which='both', axis='both')
    # Vd plot
    _plt.figure(figsize=[9.6, 7.2])
    _plt.plot(time_axis, Vd, '-x')
    _plt.title('Dump voltage')
    _plt.xlabel('Time [sec]', fontsize=14)
    _plt.ylabel('Voltage [V]', fontsize=14)
    _plt.minorticks_on()
    _plt.grid(which='both', axis='both')
    # Eq plot
    _plt.figure(figsize=[9.6, 7.2])
    _plt.plot(time_axis, Eq, '-x')
    _plt.title('Quench energy')
    _plt.xlabel('Time [sec]', fontsize=14)
    _plt.ylabel('Energy [J]', fontsize=14)
    _plt.minorticks_on()
    _plt.grid(which='both', axis='both')
    # Tmax plot
    _plt.figure(figsize=[9.6, 7.2])
    _plt.plot(time_axis, Tmax, '-x')
    _plt.title('Hot-spot temperature')
    _plt.xlabel('Time [sec]', fontsize=14)
    _plt.ylabel('Temperature [K]', fontsize=14)
    _plt.minorticks_on()
    _plt.grid(which='both', axis='both')
    # Tavg plot
    _plt.figure(figsize=[9.6, 7.2])
    _plt.plot(time_axis, Tavg, '-x')
    _plt.title('Average quench zone temperature')
    _plt.xlabel('Time [sec]', fontsize=14)
    _plt.ylabel('Temperature [K]', fontsize=14)
    _plt.minorticks_on()
    _plt.grid(which='both', axis='both')
    # zone long radius plot
    _plt.figure(figsize=[9.6, 7.2])
    _plt.plot(time_axis, final_zone_long_radius, '-x')
    _plt.title('Longitudinal zone growth')
    _plt.xlabel('Time [sec]', fontsize=14)
    _plt.ylabel('Longitudinal radius [m]', fontsize=14)
    _plt.minorticks_on()
    _plt.grid(which='both', axis='both')
    # zone transv radius plot
    _plt.figure(figsize=[9.6, 7.2])
    _plt.plot(time_axis, final_zone_transv_radius, '-x')
    _plt.title('Transverse zone growth')
    _plt.xlabel('Time [sec]', fontsize=14)
    _plt.ylabel('Transverse radius [m]', fontsize=14)
    _plt.minorticks_on()
    _plt.grid(which='both', axis='both')
    # show plots
    _plt.show()
    # Success
    return

if __name__ == "__main__":
    # Superbend
    #Iop = 124
    #Tcs = 6.0
    #Top = 5.0
    #s_cu = 2.94e-7
    #s_nbti = 2.1e-7
    #s_insulator = 3.47e-7
    #L = 4.32
    #t_dump = 0.2
    #R_dump = 4.6875
    #time_step = 0.001
    #alpha = 0.03
    #B = 6
    #RRR = 50
    #geometry = 'line'
    #magnet_vol = 0.019502
    #curr_tol = 1

    # SWLS - Model V5.0
    Iop = 275
    Tcs = 6.06
    Top = 5.0
    s_cu = 2.682e-7
    s_nbti = 2.98e-7
    #s_insulator = 6.308e-8
    s_insulator = 0
    L = 0.0997
    t_dump = 0.1
    R_dump = 2.18
    time_step = 0.0001
    alpha = 0.03
    B = 5.12
    RRR = 50
    geometry = 'line'
    magnet_vol = 616 * (s_cu + s_nbti)
    curr_tol = 1

    simple_quench_propagation(
        I_op=Iop, T_cs=Tcs, T_op=Top, copper_area=s_cu,
        nbti_area=s_nbti, insulator_area=s_insulator,
        inductance=L, magnet_vol=magnet_vol, t_dump=t_dump,
        R_dump=R_dump, time_step=time_step, RRR=RRR,
        B=B, alpha=alpha, tolerance=curr_tol, geometry=geometry
        )
