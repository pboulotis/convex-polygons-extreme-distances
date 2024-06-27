import streamlit as st
import numpy as np
import plotly.graph_objs as go
from algorithm_init import get_p_q_lists
from polygon_handling import visualise_polygons, draw_vertices
from geometry_utils import euclidean_distance, get_orthogonal_projection


def handle_case_2(greater_list, lesser_list, points):
    points.append([greater_list[0], lesser_list[0]])
    points.append([greater_list[1], lesser_list[0]])

    projection = get_orthogonal_projection(greater_list[0], greater_list[1], lesser_list[0])
    if projection:
        points.append([projection, lesser_list[0]])
    return points


def handle_final_cases(p_list, q_list):
    points = []
    if len(p_list) == len(q_list) == 1:
        return [[p_list[0], q_list[0]]]
    elif len(p_list) == 2 and len(q_list) == 1:
        return handle_case_2(p_list, q_list, points)
    elif len(q_list) == 2 and len(p_list) == 1:
        return handle_case_2(q_list, p_list, points)
    else:
        points = handle_case_2(p_list, q_list, points)
        return handle_case_2(q_list, p_list, points)


def find_min_distance(point_list):
    distances = []

    for i in range(len(point_list)):
        distances.append(euclidean_distance(point_list[i][0], point_list[i][1]))

    min_index = distances.index(min(distances))
    return distances[min_index], point_list[min_index]


def show_all_possible_pairs(pair_list):
    if len(pair_list) < 3:
        return
    st.write("All possible points that may realise minimum distance are highlighted below")
    figure = visualise_polygons()
    index = 0
    for pair in pair_list:
        x_vals, y_vals = zip(*pair)
        index = index + 1
        hex_color = f'#ff' + str(1500 * index)
        figure.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name=f'possible pair {index}',
                                    line=dict(color=hex_color, width=2, dash='dash')))
    st.plotly_chart(figure)
    st.write("Using euclidean distance, we will choose the points with the minimum distance")


def show_min_distance_result(show_all_possibilities=False):
    p_list, q_list = get_p_q_lists()
    point_list = handle_final_cases(p_list, q_list)
    distance, final_points = find_min_distance(point_list)

    if show_all_possibilities and len(point_list) != 1:
        show_all_possible_pairs(point_list)

    st.subheader("Minimum distance between the two convex polygons")
    figure = visualise_polygons()
    draw_vertices(figure, [final_points[0], final_points[1]], "red", "minimum distance")
    st.write(f"The minimum distance is {np.round(distance, 2)}"
             f" realised by the points {final_points[0]} and {final_points[1]}")
    st.plotly_chart(figure)
