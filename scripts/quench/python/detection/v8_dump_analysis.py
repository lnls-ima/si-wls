from tkinter import font
from turtle import color, position
import numpy as _np
import dump as _dump
import quench as _quench
import detection as _detection
import materials as _materials
from matplotlib import pyplot as _plt

from matplotlib import cm
from matplotlib.ticker import LinearLocator
from mpl_toolkits.mplot3d import axes3d

np_config_list = [
    2, 3, 4, 5, 6, 7, 8
]
ns_config_list = [
    2, 4, 6, 8
]
failure_list = [
    {'matrix' : [(0, 0)], 'name' : '1 unit', 'line' : '.'},
    {'matrix' : [(0, 0), (1, 0)], 'name' : '2 units in 1 column', 'line' : '.'},
    {'matrix' : [(0, 0), (0, 1)], 'name' : '2 units in 1 row', 'line' : '.'},
]

percent_shorted = 50

# dummy equivalent resistance
r_eq = 2 # ohm

###########################################################
# 3D plots

# default dump voltage
v_dump_default = 600 # V
# maximum dump voltage limit
v_dump_max = 900 # V
# voltage unbalance limit
v_unbalance_max = 900 # V
# minimum dump voltage limit
v_dump_min = 450 # V
# maximum resistance change
r_ratio_upper_lim = _np.divide(v_dump_max, v_dump_default)
# maximum voltage unbalance ratio
v_unbalance_ratio_lim = _np.divide(v_unbalance_max, (v_dump_default * 0.5))
# maximum resistance reduction
r_ratio_lower_lim = _np.divide(v_dump_min, v_dump_default)

# calculate the maximum number of failures
# for each configuration
valid_parallel_open_fail = []
valid_series_open_fail = []
valid_parallel_short_fail = []
valid_series_short_fail = []
for n_s in ns_config_list:
    for n_p in np_config_list:
        # parallel open failures
        lim_violation = False
        i = 0
        failure_points = []
        while not lim_violation:
            failure_points.append((i, 0))
            # if all parallel failed
            if i >= n_p:
                lim_violation = True
                continue
            r_dump = _dump.ResistorBank(n_parallel=n_p, n_series=n_s, r_eq=r_eq)
            r_eq_left_old = r_dump.get_equivalent_left_resistance()
            r_eq_right_old = r_dump.get_equivalent_right_resistance()
            r_dump.open_failure(failure_points)
            r_eq_left_new = r_dump.get_equivalent_left_resistance()
            r_eq_right_new = r_dump.get_equivalent_right_resistance()
            r_eq_new = r_dump.get_equivalent_resistance()
            r_ratio = _np.divide(r_eq_new, r_eq)
            if (
                    r_ratio > r_ratio_upper_lim
                    or r_ratio < r_ratio_lower_lim
                    or _np.divide(r_eq_left_new, r_eq_left_old) > v_unbalance_ratio_lim
                    or _np.divide(r_eq_right_new, r_eq_right_old) > v_unbalance_ratio_lim
                    ):
                    lim_violation = True
                    continue
            i += 1
        valid_parallel_open_fail.append({'num_fail' : i, 'np' : n_p, 'ns' : n_s, 'count' : n_p*n_s})
        # series open failures
        lim_violation = False
        i = 0
        failure_points = []
        while not lim_violation:
            failure_points.append((0, i))
            # if all series failed
            if i >= n_s:
                lim_violation = True
                continue
            r_dump = _dump.ResistorBank(n_parallel=n_p, n_series=n_s, r_eq=r_eq)
            r_eq_left_old = r_dump.get_equivalent_left_resistance()
            r_eq_right_old = r_dump.get_equivalent_right_resistance()
            r_dump.open_failure(failure_points)
            r_eq_left_new = r_dump.get_equivalent_left_resistance()
            r_eq_right_new = r_dump.get_equivalent_right_resistance()
            r_eq_new = r_dump.get_equivalent_resistance()
            r_ratio = _np.divide(r_eq_new, r_eq)
            if (
                    r_ratio > r_ratio_upper_lim
                    or r_ratio < r_ratio_lower_lim
                    or _np.divide(r_eq_left_new, r_eq_left_old) > v_unbalance_ratio_lim
                    or _np.divide(r_eq_right_new, r_eq_right_old) > v_unbalance_ratio_lim
                    ):
                    lim_violation = True
                    continue
            i += 1
        valid_series_open_fail.append({'num_fail' : i, 'np' : n_p, 'ns' : n_s, 'count' : n_p*n_s})
        # parallel short failures
        lim_violation = False
        i = 0
        failure_points = []
        while not lim_violation:
            failure_points.append((i, 0))
            # if all parallel failed
            if i >= n_p:
                lim_violation = True
                continue
            r_dump = _dump.ResistorBank(n_parallel=n_p, n_series=n_s, r_eq=r_eq)
            r_eq_left_old = r_dump.get_equivalent_left_resistance()
            r_eq_right_old = r_dump.get_equivalent_right_resistance()
            r_dump.short_failure(failure_points, per=percent_shorted)
            r_eq_left_new = r_dump.get_equivalent_left_resistance()
            r_eq_right_new = r_dump.get_equivalent_right_resistance()
            r_eq_new = r_dump.get_equivalent_resistance()
            r_ratio = _np.divide(r_eq_new, r_eq)
            if (
                    r_ratio > r_ratio_upper_lim
                    or r_ratio < r_ratio_lower_lim
                    or _np.divide(r_eq_left_new, r_eq_left_old) > v_unbalance_ratio_lim
                    or _np.divide(r_eq_right_new, r_eq_right_old) > v_unbalance_ratio_lim
                    ):
                    lim_violation = True
                    continue
            i += 1
        valid_parallel_short_fail.append({'num_fail' : i, 'np' : n_p, 'ns' : n_s, 'count' : n_p*n_s})
        # series short failures
        lim_violation = False
        i = 0
        failure_points = []
        while not lim_violation:
            failure_points.append((0, i))
            # if all series failed
            if i >= n_s:
                lim_violation = True
                continue
            r_dump = _dump.ResistorBank(n_parallel=n_p, n_series=n_s, r_eq=r_eq)
            r_eq_left_old = r_dump.get_equivalent_left_resistance()
            r_eq_right_old = r_dump.get_equivalent_right_resistance()
            r_dump.short_failure(failure_points, per=percent_shorted)
            r_eq_left_new = r_dump.get_equivalent_left_resistance()
            r_eq_right_new = r_dump.get_equivalent_right_resistance()
            r_eq_new = r_dump.get_equivalent_resistance()
            r_ratio = _np.divide(r_eq_new, r_eq)
            if (
                    r_ratio > r_ratio_upper_lim
                    or r_ratio < r_ratio_lower_lim
                    or _np.divide(r_eq_left_new, r_eq_left_old) > v_unbalance_ratio_lim
                    or _np.divide(r_eq_right_new, r_eq_right_old) > v_unbalance_ratio_lim
                    ):
                    lim_violation = True
                    continue
            i += 1
        valid_series_short_fail.append({'num_fail' : i, 'np' : n_p, 'ns' : n_s, 'count' : n_p*n_s})

parallel_open_fail_cnt_matrix = _np.reshape(
    _np.array([config['num_fail'] for config in valid_parallel_open_fail]),
    (len(ns_config_list), len(np_config_list))
    )
series_open_fail_cnt_matrix = _np.reshape(
    _np.array([config['num_fail'] for config in valid_series_open_fail]),
    (len(ns_config_list), len(np_config_list))
    )
parallel_short_fail_cnt_matrix = _np.reshape(
    _np.array([config['num_fail'] for config in valid_parallel_short_fail]),
    (len(ns_config_list), len(np_config_list))
    )
series_short_fail_cnt_matrix = _np.reshape(
    _np.array([config['num_fail'] for config in valid_series_short_fail]),
    (len(ns_config_list), len(np_config_list))
    )
parallel_resistor_cnt_matrix = _np.reshape(
    _np.array([config['count'] for config in valid_parallel_open_fail]),
    (len(ns_config_list), len(np_config_list))
    )
series_resistor_cnt_matrix = _np.reshape(
    _np.array([config['count'] for config in valid_series_open_fail]),
    (len(ns_config_list), len(np_config_list))
    )

x1, x2 = _np.meshgrid(
        _np.array(np_config_list),
        _np.array(ns_config_list)
        )
# open parallel
fig, ax1 = _plt.subplots(subplot_kw={"projection": "3d"})
surf1 = ax1.plot_surface(
    x1,
    x2,
    parallel_open_fail_cnt_matrix,
    cmap=cm.coolwarm,
    linewidth=0,
    antialiased=False
    )
ax1.set_title('Max parallel open failures supported' )
ax1.set_xlabel('Parallel count')
ax1.set_ylabel('Series count')
ax1.set_zlabel('Max parallel open failure count')
_plt.colorbar(surf1, shrink=0.5, aspect=5, pad=0.1)
# open series
fig, ax2 = _plt.subplots(subplot_kw={"projection": "3d"})
surf2 = ax2.plot_surface(
    x1,
    x2,
    series_open_fail_cnt_matrix,
    cmap=cm.coolwarm,
    linewidth=0,
    antialiased=False
    )
ax2.set_title('Max series open failures supported' )
ax2.set_xlabel('Parallel count')
ax2.set_ylabel('Series count')
ax2.set_zlabel('Max series open failure count')
_plt.colorbar(surf2, shrink=0.5, aspect=5, pad=0.1)
# combined open failure robustness
combined_open_fail_cnt_matrix = _np.minimum(
        parallel_open_fail_cnt_matrix, series_open_fail_cnt_matrix
        )
fig, ax3 = _plt.subplots(subplot_kw={"projection": "3d"})
surf3 = ax3.plot_surface(
    x1,
    x2,
    combined_open_fail_cnt_matrix,
    cmap=cm.coolwarm,
    linewidth=0,
    antialiased=False
    )
ax3.set_title('Combined max open failures supported')
ax3.set_xlabel('Parallel count')
ax3.set_ylabel('Series count')
ax3.set_zlabel('Max open failure count')
_plt.colorbar(surf3, shrink=0.5, aspect=5, pad=0.1)
# short parallel
fig, ax4 = _plt.subplots(subplot_kw={"projection": "3d"})
surf4 = ax4.plot_surface(
    x1,
    x2,
    parallel_short_fail_cnt_matrix,
    cmap=cm.coolwarm,
    linewidth=0,
    antialiased=False
    )
ax4.set_title('Max parallel short failures supported' )
ax4.set_xlabel('Parallel count')
ax4.set_ylabel('Series count')
ax4.set_zlabel('Max parallel short failure count')
_plt.colorbar(surf4, shrink=0.5, aspect=5, pad=0.1)
# short series
fig, ax5 = _plt.subplots(subplot_kw={"projection": "3d"})
surf5 = ax5.plot_surface(
    x1,
    x2,
    series_short_fail_cnt_matrix,
    cmap=cm.coolwarm,
    linewidth=0,
    antialiased=False
    )
ax5.set_title('Max series short failures supported' )
ax5.set_xlabel('Parallel count')
ax5.set_ylabel('Series count')
ax5.set_zlabel('Max series short failure count')
_plt.colorbar(surf5, shrink=0.5, aspect=5, pad=0.1)
# combined short failure robustness
combined_short_fail_cnt_matrix = _np.minimum(
        parallel_short_fail_cnt_matrix, series_short_fail_cnt_matrix
        )
fig, ax6 = _plt.subplots(subplot_kw={"projection": "3d"})
surf6 = ax6.plot_surface(
    x1,
    x2,
    combined_short_fail_cnt_matrix,
    cmap=cm.coolwarm,
    linewidth=0,
    antialiased=False
    )
ax6.set_title('Combined max short failures supported' )
ax6.set_xlabel('Parallel count')
ax6.set_ylabel('Series count')
ax6.set_zlabel('Max short failure count')
_plt.colorbar(surf6, shrink=0.5, aspect=5, pad=0.1)
# resistor count to open failure ratio
fig, ax7 = _plt.subplots(subplot_kw={"projection": "3d"})
surf7 = ax7.plot_surface(
    x1,
    x2,
    _np.divide(parallel_resistor_cnt_matrix, combined_open_fail_cnt_matrix),
    cmap=cm.coolwarm,
    linewidth=0,
    antialiased=False
    )
ax7.set_title('Resistor count to max number of open failures' )
ax7.set_xlabel('Parallel count')
ax7.set_ylabel('Series count')
ax7.set_zlabel('R_count / max_num_failures')
_plt.colorbar(surf7, shrink=0.5, aspect=5, pad=0.1)
# resistor count to short failure ratio
fig, ax8 = _plt.subplots(subplot_kw={"projection": "3d"})
surf8 = ax8.plot_surface(
    x1,
    x2,
    _np.divide(series_resistor_cnt_matrix, combined_short_fail_cnt_matrix),
    cmap=cm.coolwarm,
    linewidth=0,
    antialiased=False
    )
ax8.set_title('Resistor count to max number of short failures' )
ax8.set_xlabel('Parallel count')
ax8.set_ylabel('Series count')
ax8.set_zlabel('R_count / max_num_failures')
_plt.colorbar(surf8, shrink=0.5, aspect=5, pad=0.1)
_plt.show()


# plot resistor count for each configuration
fig, ax1 = _plt.subplots(subplot_kw={"projection": "3d"})
x1 = []
x2 = []
y = []
res_cnt = []
for n_s in ns_config_list:
    y.append([])
    res_cnt.append([])
    for n_p in np_config_list:
        r_dump = _dump.ResistorBank(n_parallel=n_p, n_series=n_s, r_eq=r_eq)
        r_eq_left_new = r_dump.get_equivalent_left_resistance()
        r_eq_right_new = r_dump.get_equivalent_right_resistance()
        r_eq_new = r_dump.get_equivalent_resistance()
        y[-1].append(100 * _np.divide(r_eq_new, r_eq))
        res_cnt[-1].append(n_p*n_s)
# plot resistor count per config
x1, x2 = _np.meshgrid(np_config_list, ns_config_list)
surf1 = ax1.plot_surface(
    x1,
    x2,
    _np.array(res_cnt),
    cmap=cm.coolwarm,
    linewidth=0,
    antialiased=False
    )
ax1.set_title('Configurations resistor count' )
ax1.set_xlabel('Parallel count')
ax1.set_ylabel('Series count')
ax1.set_zlabel('Resistor count')
_plt.colorbar(surf1, shrink=0.5, aspect=5, pad=0.1)
_plt.show()

# plot open failures: Resistance change
for failure in failure_list:
    fig, ax1 = _plt.subplots(subplot_kw={"projection": "3d"})
    x1 = []
    x2 = []
    y = []
    res_cnt = []
    for n_s in ns_config_list:
        y.append([])
        res_cnt.append([])
        for n_p in np_config_list:
            r_dump = _dump.ResistorBank(n_parallel=n_p, n_series=n_s, r_eq=r_eq)
            r_dump.open_failure(failure['matrix'])
            r_eq_left_new = r_dump.get_equivalent_left_resistance()
            r_eq_right_new = r_dump.get_equivalent_right_resistance()
            r_eq_new = r_dump.get_equivalent_resistance()
            y[-1].append(100 * _np.divide(r_eq_new, r_eq))
            res_cnt[-1].append(n_p*n_s)
    # plot change in r_eq
    x1, x2 = _np.meshgrid(np_config_list, ns_config_list)
    surf1 = ax1.plot_surface(
        x1,
        x2,
        _np.array(y),
        cmap=cm.coolwarm,
        linewidth=0,
        antialiased=False
        )
    ax1.set_title('Resistance variation: Open '+failure['name'])
    ax1.set_xlabel('Parallel count')
    ax1.set_ylabel('Series count')
    ax1.set_zlabel('R_eq [%]')
    _plt.colorbar(surf1, shrink=0.5, aspect=5, pad=0.1)
    _plt.show()

# plot open failures: Voltage unbalance
for failure in failure_list:
    fig, ax1 = _plt.subplots(subplot_kw={"projection": "3d"})
    x1 = []
    x2 = []
    v_divider = []
    res_cnt = []
    for n_s in ns_config_list:
        v_divider.append([])
        for n_p in np_config_list:
            r_dump = _dump.ResistorBank(n_parallel=n_p, n_series=n_s, r_eq=r_eq)
            r_dump.open_failure(failure['matrix'])
            r_eq_left_new = r_dump.get_equivalent_left_resistance()
            r_eq_right_new = r_dump.get_equivalent_right_resistance()
            r_eq_new = r_dump.get_equivalent_resistance()
            v_divider[-1].append(100 * _np.divide(r_eq_left_new, r_eq_new))
    # plot change in v_percent
    x1, x2 = _np.meshgrid(np_config_list, ns_config_list)
    surf1 = ax1.plot_surface(
        x1,
        x2,
        _np.array(v_divider),
        cmap=cm.coolwarm,
        linewidth=0,
        antialiased=False
        )
    ax1.set_title('Voltage unbalance: Open '+failure['name'])
    ax1.set_xlabel('Parallel count')
    ax1.set_ylabel('Series count')
    ax1.set_zlabel('Voltage divider [%]', color='tab:red')
    _plt.colorbar(surf1, shrink=0.5, aspect=5, pad=0.1)
    _plt.show()

# plot short failures: Resistance change
for failure in failure_list:
    fig, ax1 = _plt.subplots(subplot_kw={"projection": "3d"})
    x1 = []
    x2 = []
    y = []
    for n_s in ns_config_list:
        y.append([])
        for n_p in np_config_list:
            r_dump = _dump.ResistorBank(n_parallel=n_p, n_series=n_s, r_eq=r_eq)
            r_eq_left_old = r_dump.get_equivalent_left_resistance()
            r_eq_right_old = r_dump.get_equivalent_right_resistance()
            r_dump.short_failure(failure['matrix'], per=percent_shorted)
            r_eq_left_new = r_dump.get_equivalent_left_resistance()
            r_eq_right_new = r_dump.get_equivalent_right_resistance()
            r_eq_new = r_dump.get_equivalent_resistance()
            y[-1].append(100 * _np.divide(r_eq_new, r_eq))
    # plot change in r_eq
    x1, x2 = _np.meshgrid(np_config_list, ns_config_list)
    surf1 = ax1.plot_surface(
        x1,
        x2,
        _np.array(y),
        cmap=cm.coolwarm,
        linewidth=0,
        antialiased=False
        )
    ax1.set_title(
        "Resistance variation: Short of {}% of {}".format(
            percent_shorted, failure['name']
            )
    )
    ax1.set_xlabel('Parallel count')
    ax1.set_ylabel('Series count')
    ax1.set_zlabel('R_eq [%]')
    _plt.colorbar(surf1, shrink=0.5, aspect=5, pad=0.1)
    _plt.show()

# plot short failures: Voltage unbalance
for failure in failure_list:
    fig, ax1 = _plt.subplots(subplot_kw={"projection": "3d"})
    x1 = []
    x2 = []
    v_divider = []
    for n_s in ns_config_list:
        v_divider.append([])
        for n_p in np_config_list:
            r_dump = _dump.ResistorBank(n_parallel=n_p, n_series=n_s, r_eq=r_eq)
            r_dump.short_failure(failure['matrix'], per=percent_shorted)
            r_eq_left_new = r_dump.get_equivalent_left_resistance()
            r_eq_right_new = r_dump.get_equivalent_right_resistance()
            r_eq_new = r_dump.get_equivalent_resistance()
            v_divider[-1].append(100 * _np.divide(r_eq_left_new, r_eq_new))
    # plot change in v_percent
    x1, x2 = _np.meshgrid(np_config_list, ns_config_list)
    surf1 = ax1.plot_surface(
        x1,
        x2,
        _np.array(v_divider),
        cmap=cm.coolwarm,
        linewidth=0,
        antialiased=False
        )
    ax1.set_title(
            "Voltage unbalance: Short of {}% of {}".format(
            percent_shorted, failure['name']
            )
        )
    ax1.set_xlabel('Parallel count')
    ax1.set_ylabel('Series count')
    ax1.set_zlabel('Voltage divider [%]', color='tab:red')
    _plt.colorbar(surf1, shrink=0.5, aspect=5, pad=0.1)
    _plt.show()

###########################################################
# 2D plots

# plot open failures (combined plot)
for failure in failure_list:
    fig, ax1 = _plt.subplots()
    ax2 = ax1.twinx()
    x = []
    y = []
    v_divider = []
    res_cnt = []
    for n_s in ns_config_list:
        for n_p in np_config_list:
            r_dump = _dump.ResistorBank(n_parallel=n_p, n_series=n_s, r_eq=r_eq)
            r_dump.open_failure(failure['matrix'])
            r_eq_left_new = r_dump.get_equivalent_left_resistance()
            r_eq_right_new = r_dump.get_equivalent_right_resistance()
            r_eq_new = r_dump.get_equivalent_resistance()
            y.append(100 * _np.divide(r_eq_new, r_eq))
            x.append("({}, {})".format(n_p, n_s))
            v_divider.append(100*_np.divide(r_eq_left_new, r_eq_new))
            res_cnt.append(
                {'x':x[-1], 'y':y[-1], 'cnt':n_p*n_s}
                )
    # plot change in r_eq
    ax1.plot(
        x,
        y,
        failure['line']
        )
    ax2.plot(
        x,
        v_divider,
        failure['line'],
        color='tab:red'
    )
    for info in res_cnt:
        ax1.annotate(str(info['cnt']), (info['x'],info['y']), fontsize=11)
    ax1.set_title('Combined data: Open '+failure['name'])
    ax1.set_ylabel('R_eq [%]', color='tab:blue')
    ax1.set_xlabel('Configuration (num_parallel, num_series)')
    ax2.set_ylabel('Voltage divider [%]', color='tab:red')
    ax1.minorticks_on()
    ax1.grid(which='both', axis='both')
    ax1.text(
        x[0], y[-1], "# of resistors in config indicated",
        fontdict=dict(size='11'),
        bbox=dict(facecolor='white', alpha=1.0)
        )
    fig.tight_layout()
    _plt.show()

# plot open failures: Resistance change
for failure in failure_list:
    fig, ax1 = _plt.subplots()
    x = []
    y = []
    res_cnt = []
    for n_s in ns_config_list:
        for n_p in np_config_list:
            r_dump = _dump.ResistorBank(n_parallel=n_p, n_series=n_s, r_eq=r_eq)
            r_dump.open_failure(failure['matrix'])
            r_eq_left_new = r_dump.get_equivalent_left_resistance()
            r_eq_right_new = r_dump.get_equivalent_right_resistance()
            r_eq_new = r_dump.get_equivalent_resistance()
            y.append(100 * _np.divide(r_eq_new, r_eq))
            x.append("({}, {})".format(n_p, n_s))
            res_cnt.append(
                {'x':x[-1], 'y':y[-1], 'cnt':n_p*n_s}
                )
    # plot change in r_eq
    ax1.plot(
        x,
        y,
        failure['line']
        )
    for info in res_cnt:
        ax1.annotate(str(info['cnt']), (info['x'],info['y']), fontsize=11)
    ax1.set_title('Resistance variation: Open '+failure['name'])
    ax1.set_ylabel('R_eq [%]', color='tab:blue')
    ax1.set_xlabel('Configuration (num_parallel, num_series)')
    ax1.minorticks_on()
    ax1.grid(which='both', axis='both')
    ax1.text(
        x[0], y[-1], "# of resistors in config indicated",
        fontdict=dict(size='11'),
        bbox=dict(facecolor='white', alpha=1.0)
        )
    fig.tight_layout()
    _plt.show()

# plot open failures: Voltage unbalance
for failure in failure_list:
    fig, ax1 = _plt.subplots()
    x = []
    v_divider = []
    res_cnt = []
    for n_s in ns_config_list:
        for n_p in np_config_list:
            r_dump = _dump.ResistorBank(n_parallel=n_p, n_series=n_s, r_eq=r_eq)
            r_dump.open_failure(failure['matrix'])
            r_eq_left_new = r_dump.get_equivalent_left_resistance()
            r_eq_right_new = r_dump.get_equivalent_right_resistance()
            r_eq_new = r_dump.get_equivalent_resistance()
            v_divider.append(100 * _np.divide(r_eq_left_new, r_eq_new))
            x.append("({}, {})".format(n_p, n_s))
            res_cnt.append(
                {'x':x[-1], 'y':v_divider[-1], 'cnt':n_p*n_s}
                )
    # plot change in r_eq
    ax1.plot(
        x,
        v_divider,
        failure['line'],
        color='tab:red'
        )
    for info in res_cnt:
        ax1.annotate(str(info['cnt']), (info['x'],info['y']), fontsize=11)
    ax1.set_title('Voltage unbalance: Open '+failure['name'])
    ax1.set_ylabel('Voltage divider [%]', color='tab:red')
    ax1.set_xlabel('Configuration (num_parallel, num_series)')
    ax1.minorticks_on()
    ax1.grid(which='both', axis='both')
    ax1.text(
        x[0], y[-1], "# of resistors in config indicated",
        fontdict=dict(size='11'),
        bbox=dict(facecolor='white', alpha=1.0)
        )
    fig.tight_layout()
    _plt.show()

# plot short failures (combined data)
percent_shorted = 50
for failure in failure_list:
    fig, ax1 = _plt.subplots()
    ax2 = ax1.twinx()
    x = []
    y = []
    v_divider = []
    res_cnt = []
    for n_s in ns_config_list:
        for n_p in np_config_list:
            r_dump = _dump.ResistorBank(n_parallel=n_p, n_series=n_s, r_eq=r_eq)
            r_dump.short_failure(failure['matrix'], per=percent_shorted)
            r_eq_left_new = r_dump.get_equivalent_left_resistance()
            r_eq_right_new = r_dump.get_equivalent_right_resistance()
            r_eq_new = r_dump.get_equivalent_resistance()
            y.append(100 * _np.divide(r_eq_new, r_eq))
            x.append("({}, {})".format(n_p, n_s))
            v_divider.append(100 * _np.divide(r_eq_left_new, r_eq_new))
            res_cnt.append(
                {'x':x[-1], 'y':y[-1], 'cnt':n_p*n_s}
                )
    ax1.plot(
        x,
        y,
        failure['line'],
        color='tab:blue'
        )
    ax2.plot(
        x,
        v_divider,
        failure['line'],
        color='tab:red'
        )
    for info in res_cnt:
        ax1.annotate(str(info['cnt']), (info['x'],info['y']), fontsize=11)
    ax1.set_title(
        "Combined data: Short of {}% of {}".format(
            percent_shorted, failure['name']
            )
        )
    ax1.set_ylabel('R_eq [%]')
    ax1.set_xlabel('Configuration (num_parallel, num_series)')
    ax2.set_ylabel('Voltage divider [%]')
    ax1.minorticks_on()
    ax1.grid(which='both', axis='both')
    ax1.text(
        x[0], y[-1], "# of resistors in config indicated",
        fontdict=dict(size='11'),
        bbox=dict(facecolor='white', alpha=1.0)
        )
    #_plt.tight_layout()
    _plt.show()

# plot short failures: Resistance change
percent_shorted = 50
for failure in failure_list:
    fig, ax1 = _plt.subplots()
    x = []
    y = []
    res_cnt = []
    for n_s in ns_config_list:
        for n_p in np_config_list:
            r_dump = _dump.ResistorBank(n_parallel=n_p, n_series=n_s, r_eq=r_eq)
            r_dump.short_failure(failure['matrix'], per=percent_shorted)
            r_eq_left_new = r_dump.get_equivalent_left_resistance()
            r_eq_right_new = r_dump.get_equivalent_right_resistance()
            r_eq_new = r_dump.get_equivalent_resistance()
            y.append(100 * _np.divide(r_eq_new, r_eq))
            x.append("({}, {})".format(n_p, n_s))
            res_cnt.append(
                {'x':x[-1], 'y':y[-1], 'cnt':n_p*n_s}
                )
    ax1.plot(
        x,
        y,
        failure['line'],
        color='tab:blue'
        )
    for info in res_cnt:
        ax1.annotate(str(info['cnt']), (info['x'],info['y']), fontsize=11)
    ax1.set_title(
        "Resistance variation: Short of {}% of {}".format(
            percent_shorted, failure['name']
            )
        )
    ax1.set_ylabel('R_eq [%]')
    ax1.set_xlabel('Configuration (num_parallel, num_series)')
    ax1.minorticks_on()
    ax1.grid(which='both', axis='both')
    ax1.text(
        x[0], y[-1], "# of resistors in config indicated",
        fontdict=dict(size='11'),
        bbox=dict(facecolor='white', alpha=1.0)
        )
    #_plt.tight_layout()
    _plt.show()

# plot short failures: Voltage unbalance
percent_shorted = 50
for failure in failure_list:
    fig, ax1 = _plt.subplots()
    x = []
    v_divider = []
    res_cnt = []
    for n_s in ns_config_list:
        for n_p in np_config_list:
            r_dump = _dump.ResistorBank(n_parallel=n_p, n_series=n_s, r_eq=r_eq)
            r_dump.short_failure(failure['matrix'], per=percent_shorted)
            r_eq_left_new = r_dump.get_equivalent_left_resistance()
            r_eq_right_new = r_dump.get_equivalent_right_resistance()
            r_eq_new = r_dump.get_equivalent_resistance()
            x.append("({}, {})".format(n_p, n_s))
            v_divider.append(100 * _np.divide(r_eq_left_new, r_eq_new))
            res_cnt.append(
                {'x':x[-1], 'y':v_divider[-1], 'cnt':n_p*n_s}
                )
    ax1.plot(
        x,
        v_divider,
        failure['line'],
        color='tab:red'
        )
    for info in res_cnt:
        ax1.annotate(str(info['cnt']), (info['x'],info['y']), fontsize=11)
    ax1.set_title(
        "Voltage unbalance: Short of {}% of {}".format(
            percent_shorted, failure['name']
            )
        )
    ax1.set_xlabel('Configuration (num_parallel, num_series)')
    ax1.set_ylabel('Voltage divider [%]')
    ax1.minorticks_on()
    ax1.grid(which='both', axis='both')
    ax1.text(
        x[0], y[-1], "# of resistors in config indicated",
        fontdict=dict(size='11'),
        bbox=dict(facecolor='white', alpha=1.0)
        )
    #_plt.tight_layout()
    _plt.show()
