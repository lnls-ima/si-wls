import sys as _sys
import traceback as _traceback
import numpy as _np
from matplotlib import pyplot as _plt
import detection as _detection
import materials as _materials

CU_PROPERTIES = _materials.Copper()
NBTI_PROPERTIES = _materials.NbTi()

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

def nbti_avg_heat_capacity_below_9K(T2, T1, B):
    # Definite integral of the C_nbti equation
    # provided at:
    #     Akbar and Keller, "Thermal Analysis
    #     and Simulation of the Superconducting
    #     Magnet in the SpinQuestExperiment at Fermilab"
    #
    # C_nbti = definite integral from T1 to T2 of
    #          (0.0082*T^3 + 0.011*B*T)
    #
    return _np.divide(
            0.00205 * (_np.power(T2,4) - _np.power(T1,4))
            + 0.0055 * B * (_np.power(T2,2) - _np.power(T1,2)),
            T2 - T1
            )

def nbti_heat_capacity_below_9k(temp, B):
    return 0.0082*_np.power(temp,3) + 0.011*B*temp

def cu_avg_heat_capacity(T2, T1, num_steps=1000):
    x = _np.linspace(T1, T2, num=num_steps, endpoint=True)
    y = _np.array([CU_PROPERTIES.calc_specific_heat(i) for i in x])
    integral_val = _np.trapz(y, x)
    return integral_val / (T2 - T1)

def composite_heat_capacity_below_9k(copper_area, nbti_area, T_joule, T_op, B):
    # calculate average Cu heat capacity
    C_cu = cu_avg_heat_capacity(T_joule, T_op)
    # calculate average Nb-Ti heat capacity
    C_nbti = nbti_avg_heat_capacity_below_9K(T_joule, T_op, B)
    # return average composite heat capacity
    return (
        (C_cu*copper_area + C_nbti*nbti_area)
        / (copper_area + nbti_area)
    )

def composite_heat_capacity(copper_area, nbti_area, temp):
    # calculate Cu heat capacity
    C_cu = CU_PROPERTIES.calc_specific_heat(temp)
    # calculate Nb-Ti heat capacity
    C_nbti = NBTI_PROPERTIES.calc_specific_heat_broad_range(temp)
    # return composite heat capacity
    return (C_cu*copper_area + C_nbti*nbti_area) / (copper_area + nbti_area)

def composite_density(copper_area, nbti_area):
    return (
        (CU_PROPERTIES.density*copper_area + NBTI_PROPERTIES.density*nbti_area)
        / (copper_area + nbti_area)
    )

def nbti_avg_thermal_conductivity(T2, T1, num_steps=1000):
    x = _np.linspace(T1, T2, num=num_steps, endpoint=True)
    y = _np.array([NBTI_PROPERTIES.calc_thermal_conductivity(i) for i in x])
    integral_val = _np.trapz(y, x)
    return integral_val / (T2 - T1)

def cu_avg_thermal_conductivity(T2, T1, RRR, num_steps=1000):
    x = _np.linspace(T1, T2, num=num_steps, endpoint=True)
    y = _np.array([CU_PROPERTIES.calc_thermal_conductivity(i, RRR) for i in x])
    integral_val = _np.trapz(y, x)
    return integral_val / (T2 - T1)

def composite_thermal_conductivity(copper_area, nbti_area, T2, T1, RRR):
    # avg Nb-Ti k
    k_nbti = nbti_avg_thermal_conductivity(T2, T1)
    # avg Cu k
    k_cu = cu_avg_thermal_conductivity(T2, T1, RRR)
    # composite result
    return (k_cu*copper_area + k_nbti*nbti_area) / (copper_area + nbti_area)

def heating_factor(
        J, temp, copper_area, nbti_area, RRR, B):
    # resistivity
    rho = CU_PROPERTIES.calc_resistivity(temp, RRR, B)
    # density
    dsty_avg = composite_density(copper_area, nbti_area)
    # heat capacity
    c_avg = composite_heat_capacity(copper_area, nbti_area, temp)
    # DEBUG
    #heat = (_np.power(J, 2) * rho) / (dsty_avg * c_avg)
    #print('J = {0}, rho = {1}, dsty_avg = {2}, c_avg = {3}, heat = {4}'.format(J, rho, dsty_avg, c_avg,heat))
    # result
    return (_np.power(J, 2) * rho) / (dsty_avg * c_avg)

def geometric_factor(
        transv_radius, long_radius,
        hole_transv_radius, hole_long_radius,
        copper_area, nbti_area, insulator_area):
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

def ellipsoid_vol(a, b):
    # calculate ellipsoid volume
    return 4/3 * _np.pi * _np.power(b, 2) * a

def quench_propagation(
        I_op, T_joule, T_op, copper_area, nbti_area, insulator_area,
        inductance, magnet_vol, t_dump=0, r_dump=0, time_step=0.000001, RRR=100,
        B=0, alpha=0.03, tolerance=1e-6
        ):
    """
       Refs.: 
       [1] M. Wilson, "Lecture 4: Quenching and Protection", JUAS, February 2016. """
    # quench evolution output variables
    iter_cnt = 0
    zone_list = []
    I = []
    R = []
    final_zone_transv_radius = []
    final_zone_long_radius = []
    # initial condition
    propagation_end = False
    I.append(I_op)
    R.append(0)
    final_zone_long_radius.append(0)
    final_zone_transv_radius.append(0)
    # select initial resistivity based on RRR
    rho_0 = CU_PROPERTIES.calc_resistivity(T_joule, RRR, B)
    # create initial zone
    zone_list.append(
        QuenchZone(
            long_radius=0, transv_radius=0,
            hole_long_radius=0, hole_transv_radius=0,
            T=T_joule, rho=rho_0, R=0
        )
    )
    # calculate initial current density
    J0 = I_op / (copper_area + nbti_area)
    # calculate average heat capacity
    C_avg = composite_heat_capacity_below_9k(
        copper_area, nbti_area, T_joule, T_op, B
    )
    # calculate avg composite density
    dsty_avg = composite_density(copper_area, nbti_area)
    # calculate avg thermal conductivity below 9 K
    k_avg = composite_thermal_conductivity(
        copper_area, nbti_area, T_joule, T_op, RRR
    )
    # calculate prop velocity
    vq = _detection.calc_prop_velocity(
        J0, C_avg*dsty_avg, rho_0, k_avg, T_joule, T_op, 'adiabatic'
    )
    # grow zone based on vq
    zone_list[0].long_radius += vq * time_step
    zone_list[0].transv_radius += alpha * vq * time_step
    # calculate current density after quench
    J = I_op / copper_area
    # increase zone 1 temperature
    zone_list[0].T += time_step * heating_factor(
        J, zone_list[0].T, copper_area, nbti_area, RRR, B
        )
    # update zone 1 resistivity
    zone_list[0].rho = CU_PROPERTIES.calc_resistivity(
        zone_list[0].T,RRR,B
        )
    # update resistance
    zone_list[0].R = zone_list[0].rho * geometric_factor(
        zone_list[0].transv_radius, zone_list[0].long_radius,
        0, 0, copper_area, nbti_area, insulator_area
        )
    R_quench = zone_list[0].R
    # update current and add dump resistance
    if (iter_cnt*time_step >= t_dump):
        R_total = R_quench + r_dump
        I_op = I_op - I_op*(R_total/inductance)*time_step
    else:
        R_total = R_quench
        I_op = I_op
    # update current density
    J = I_op / copper_area
    # update prop velocity
    vq = _detection.calc_prop_velocity(
        (I_op / (copper_area + nbti_area)),
        C_avg*dsty_avg, rho_0, k_avg, T_joule, T_op, 'adiabatic'
    )
    # update outputs
    R.append(R_quench)
    I.append(I_op)
    final_zone_transv_radius.append(zone_list[0].transv_radius)
    final_zone_long_radius.append(zone_list[0].long_radius)
    iter_cnt += 1
    # ITERATION LOOP
    while (I_op > tolerance):
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
            if ellipsoid_vol(new_long_radius, new_transv_radius) >= magnet_vol:
                propagation_end = True
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
        # Reset R quench
        R_quench = 0
        # update zones
        for zone in zone_list:
            # increase temperature
            zone.T += time_step * heating_factor(
                J, zone.T, copper_area, nbti_area, RRR, B
                )
            # DEBUG
            #if (iter_cnt < 5):
            #    print('Temp = {0}'.format(zone.T))
            # update resistivity
            zone.rho = CU_PROPERTIES.calc_resistivity(
                zone.T, RRR, B
                )
            # update resistance
            zone.R = zone.rho * geometric_factor(
                zone.transv_radius, zone.long_radius,
                zone.hole_transv_radius,
                zone.hole_long_radius,
                copper_area, nbti_area, insulator_area
                )
            # add to R quench
            R_quench += zone.R
        # update current and add dump resistance
        if (iter_cnt*time_step >= t_dump):
            R_total = R_quench + r_dump
            I_op = (
                I_op - I_op*(R_total/inductance)*time_step
            )
        else:
            R_total = R_quench
            I_op = I_op
        # update current density
        J = I_op / copper_area
        # update prop velocity
        vq = _detection.calc_prop_velocity(
            (I_op / (copper_area + nbti_area)),
            C_avg*dsty_avg, rho_0, k_avg, T_joule, T_op, 'adiabatic'
        )
        # update outputs
        R.append(R_quench)
        I.append(I_op)
        final_zone_transv_radius.append(zone_list[-1].transv_radius)
        final_zone_long_radius.append(zone_list[-1].long_radius)
        iter_cnt += 1
        # DEBUG
        #if (iter_cnt > 5):
        #    exit()
    # print results
    time_axis = _np.arange(
        0, iter_cnt*time_step + time_step, time_step
    )
    # R quench plot
    _plt.figure()
    _plt.plot(time_axis, R, '-x')
    _plt.title('Quench resistance growth')
    _plt.xlabel('Time [sec]', fontsize=14)
    _plt.ylabel('R [ohm]', fontsize=14)
    _plt.grid(True)
    # I plot
    _plt.figure()
    _plt.plot(time_axis, I, '-x')
    _plt.title('Current decay')
    _plt.xlabel('Time [sec]', fontsize=14)
    _plt.ylabel('I [A]', fontsize=14)
    _plt.grid(True)
    # zone long radius plot
    _plt.figure()
    _plt.plot(time_axis, final_zone_long_radius, '-x')
    _plt.title('Longitudinal zone growth')
    _plt.xlabel('Time [sec]', fontsize=14)
    _plt.ylabel('Longitudinal radius [m]', fontsize=14)
    _plt.grid(True)
    # zone transv radius plot
    _plt.figure()
    _plt.plot(time_axis, final_zone_transv_radius, '-x')
    _plt.title('Transverse zone growth')
    _plt.xlabel('Time [sec]', fontsize=14)
    _plt.ylabel('Transverse radius [m]', fontsize=14)
    _plt.grid(True)
    # show plots
    _plt.show()
    # DEBUG
    print('num iter = {0}'.format(iter_cnt))
    print('max temp = {0}'.format(zone_list[0].T))
    # Success
    return

