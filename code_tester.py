from matplotlib import pyplot as plt

import init

vertices1 = [(0, 0), (0.5, 0), (1, 0.5), (0.5, 1), (0, 1), (-0.5, 0.5)]
vertices2 = [(2, 1.5), (2.5, 2.5), (1.75, 3), (1, 2.5), (1.5, 1.5)]

fig, ax = plt.subplots()
fig.subplots_adjust(bottom=0.2)

init.original_plot(vertices1, vertices2, ax)

p_prime_list, q_prime_list = init.initial_phase(vertices1, vertices2, ax)

init.plot_p_q_prime_lists(ax, vertices1, vertices2, p_prime_list, q_prime_list)

plt.show()
