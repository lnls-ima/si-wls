import dump as _dump
import quench as _quench
import detection as _detection
import materials as _materials
from matplotlib import pyplot as _plt

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

# plot open failures
for failure in failure_list:
    _plt.figure()
    x = []
    y = []
    for n_s in ns_config_list:
        for n_p in np_config_list:
            r_dump = _dump.ResistorBank(n_parallel=n_p, n_series=n_s, r_eq=r_eq)
            r_dump.open_failure(failure['matrix'])
            y.append(r_dump.get_equivalent_resistance())
            x.append("({}, {})".format(n_p, n_s))
    _plt.plot(
        x,
        y,
        failure['line']
        )
    _plt.title('Open '+failure['name'])
    _plt.show()

# plot short failures
percent_shorted = 50
for failure in failure_list:
    _plt.figure()
    x = []
    y = []
    for n_s in ns_config_list:
        for n_p in np_config_list:
            r_dump = _dump.ResistorBank(n_parallel=n_p, n_series=n_s, r_eq=r_eq)
            r_dump.short_failure(failure['matrix'], per=percent_shorted)
            y.append(r_dump.get_equivalent_resistance())
            x.append("({}, {})".format(n_p, n_s))
    _plt.plot(
        x,
        y,
        failure['line']
        )
    _plt.title("Short of {}% of {}".format(percent_shorted, failure['name']))
    _plt.show()
