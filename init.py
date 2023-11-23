from matplotlib import pyplot as plt
import utils
import shapely.geometry as sg


def original_plot(vertices1, vertices2, ax):
    ax.clear()
    polygon1, polygon2 = sg.Polygon(vertices1), sg.Polygon(vertices2)
    ax.fill(*polygon1.exterior.xy, alpha=0.5, label='P')
    ax.fill(*polygon2.exterior.xy, alpha=0.5, label='Q')
    ax.legend()
    ax.axis('equal')


def plot_tangents(ax, lower_tangent1, lower_tangent2, point1, point2, upper_tangent1, upper_tangent2):
    point_x1, point_y1 = point1
    # ax.annotate('u', (point_x1, point_y1 - 0.25), xytext=(0, 10), textcoords='offset points')
    ax.text(point_x1, point_y1 - 0.15, 'u')

    lt_x1, lt_y1 = lower_tangent1
    ax.plot([point_x1, lt_x1], [point_y1, lt_y1], 'b--', label='Q tangent lines')

    ut_x1, ut_y1 = upper_tangent1
    ax.plot([point_x1, ut_x1], [point_y1, ut_y1], 'b--')

    point_x2, point_y2 = point2
    ax.text(point_x2, point_y2, 'w')

    lt_x2, lt_y2 = lower_tangent2
    ax.plot([point_x2, lt_x2], [point_y2, lt_y2], 'g--', label='P tangent lines')

    ut_x2, ut_y2 = upper_tangent2
    ax.plot([point_x2, ut_x2], [point_y2, ut_y2], 'g--')


def plot_p_q_prime_lists(ax, vertices1, vertices2, p_prime_list, q_prime_list):
    original_plot(vertices1, vertices2, ax)

    u_lower = p_prime_list[0]
    u_upper = p_prime_list[-1]
    ax.text(u_lower[0], u_lower[1], "u'")
    ax.text(u_upper[0], u_upper[1], "u''")

    w_lower = q_prime_list[-1]
    w_upper = q_prime_list[0]
    ax.text(w_lower[0], w_lower[1], "w'")
    ax.text(w_upper[0], w_upper[1], "w''")

    for i in range(len(p_prime_list) - 1):
        plt.plot([p_prime_list[i][0], p_prime_list[i + 1][0]],
                 [p_prime_list[i][1], p_prime_list[i + 1][1]], color='black')

    for i in range(len(q_prime_list) - 1):
        plt.plot([q_prime_list[i][0], q_prime_list[i + 1][0]],
                 [q_prime_list[i][1], q_prime_list[i + 1][1]], color='black')

    plt.draw()


def initial_phase(vertices1, vertices2, ax):
    point_u = vertices1[2]
    point_w = vertices2[2]

    # Find the tangent vertices
    lower_tangent1, upper_tangent1 = utils.find_tangents(vertices2, point_u, "u")
    lower_tangent2, upper_tangent2 = utils.find_tangents(vertices1, point_w, "w")

    plot_tangents(ax, lower_tangent1, lower_tangent2, point_u, point_w, upper_tangent1, upper_tangent2)

    u_lower, u_upper = lower_tangent2, upper_tangent2
    w_lower, w_upper = lower_tangent1, upper_tangent1

    p_prime_list = utils.get_selected_vertices(vertices1, u_lower, u_upper)
    q_prime_list = utils.get_selected_vertices(vertices2, w_upper, w_lower)

    # new_button = Button(btn, "Compute P' and Q'")
    # new_button.set_active(True)
    # new_button.on_clicked(lambda event: plot_p_q_prime_lists(ax, vertices1, vertices2, p_prime_list, q_prime_list))

    # plot_p_q_prime_lists()

    return p_prime_list, q_prime_list
