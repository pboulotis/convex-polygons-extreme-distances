import streamlit as st
# import plotly.graph_objs as go
from init import get_p_q_lists
from start import visualise_polygons, add_line
from utils import euclidean_distance, get_orthogonal_projection


def find_min_distance(point_list):
    distances = []
    for i in range(len(point_list)):
        distances.append(euclidean_distance(point_list[i][0], point_list[i][1]))

    min_index = distances.index(min(distances))
    return distances[min_index], point_list[min_index]


def show_result():
    figure = visualise_polygons()
    p_list, q_list = get_p_q_lists()
    point_list = handle_final_cases(p_list, q_list)
    distance, final_points = find_min_distance(point_list)

    add_line(figure, final_points[0], final_points[1], "red", "minimum distance")
    st.plotly_chart(figure)
    st.write(f"The minimum distance is: {distance}")


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
        return p_list[0], q_list[0]

    elif len(p_list) == 2 and len(q_list) == 1:
        return handle_case_2(p_list, q_list, points)
    elif len(q_list) == 2 and len(p_list) == 1:
        return handle_case_2(q_list, p_list, points)
    else:
        points = handle_case_2(p_list, q_list, points)
        return handle_case_2(q_list, p_list, points)
