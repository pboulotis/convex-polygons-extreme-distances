import sys
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from tkinter import messagebox
import init
import utils


def check_convex(event):
    message = 'Both polygons are convex.'
    if not utils.check_convex_polygon(vertices1):
        message = 'The P polygon is not convex.'
        messagebox.showinfo("Convexity Check:", message)
        sys.exit(1)

    if not utils.check_convex_polygon(vertices2):
        message = 'The Q polygon is not convex.'
        messagebox.showinfo("Convexity Check:", message)
        sys.exit(1)

    messagebox.showinfo("Convexity Check:", message)
    # check_button.set_active(False)
    # check_button.ax.set_visible(False)

    p_prime_list, q_prime_list = init.initial_phase(vertices1, vertices2, ax)

    ax.legend()
    plt.draw()
    check_button.label.set_text('')


if __name__ == '__main__':
    vertices1 = [(0, 0), (0.5, 0), (1, 0.5), (0.5, 1), (0, 1), (-0.5, 0.5)]
    vertices2 = [(2, 1.5), (2.5, 2.5), (1.75, 3), (1, 2.5), (1.5, 1.5)]
    vertices1 = utils.convert_counterclockwise(vertices1)
    vertices2 = utils.convert_counterclockwise(vertices2)

    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.2)

    init.original_plot(vertices1, vertices2, ax)

    step_button = fig.add_axes([0.75, 0.005, 0.2, 0.075])
    check_button = Button(step_button, 'Check Convexity')
    check_button.on_clicked(check_convex)

    # p_prime_list, q_prime_list = init.initial_phase(vertices1, vertices2, ax)

    # new_button = Button(check_button.ax, "Compute P' and Q'")
    # new_button.set_active(True)
    # new_button.on_clicked(lambda event: init.plot_p_q_prime_lists(ax, vertices1, vertices2, p_prime_list, q_prime_list))
    plt.show()
