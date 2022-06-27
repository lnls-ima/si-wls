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

# dummy equivalent resistance
r_eq = 1 # ohm

###########################################################
# 3D plots

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
        y[-1].append(100 * r_eq_new / r_eq)
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
            y[-1].append(100 * r_eq_new / r_eq)
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
percent_shorted = 50
for failure in failure_list:
    fig, ax1 = _plt.subplots(subplot_kw={"projection": "3d"})
    x1 = []
    x2 = []
    y = []
    for n_s in ns_config_list:
        y.append([])
        for n_p in np_config_list:
            r_dump = _dump.ResistorBank(n_parallel=n_p, n_series=n_s, r_eq=r_eq)
            r_dump.short_failure(failure['matrix'], per=percent_shorted)
            r_eq_left_new = r_dump.get_equivalent_left_resistance()
            r_eq_right_new = r_dump.get_equivalent_right_resistance()
            r_eq_new = r_dump.get_equivalent_resistance()
            y[-1].append(100 * r_eq_new / r_eq)
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
percent_shorted = 50
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
            y.append(100 * r_eq_new / r_eq)
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
            y.append(100 * r_eq_new / r_eq)
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
percent_shorted = 100
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
            y.append(100 * r_eq_new / r_eq)
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
percent_shorted = 100
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
            y.append(100 * r_eq_new / r_eq)
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
percent_shorted = 100
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
