import streamlit as st
import plotly.graph_objs as go
from start import add_point, add_line, add_vertices, visualize_polygons
from utils import get_neighbour_vertices, get_angle, get_selected_vertices


def show_main_figure(p_list, q_list):
    figure = visualize_polygons()

    add_vertices(figure, p_list, "green", "P'")
    figure.add_annotation(go.layout.Annotation(x=p_list[0][0], y=p_list[0][1],
                                               text="p1"))
    figure.add_annotation(go.layout.Annotation(x=p_list[-1][0], y=p_list[-1][1],
                                               text="p2"))
    add_vertices(figure, q_list, "red", "Q'")
    figure.add_annotation(go.layout.Annotation(x=q_list[0][0], y=q_list[0][1],
                                               text="q2"))
    figure.add_annotation(go.layout.Annotation(x=q_list[-1][0], y=q_list[-1][1],
                                               text="q1"))

    show_medians(p_list, q_list, figure)
    st.plotly_chart(figure)


def show_medians(p_list, q_list, figure):
    mp = p_list[len(p_list) // 2]
    mq = q_list[len(q_list) // 2]

    st.write("We compute the median mp in the P' list as well as the median mq in the Q' list."
             " Thus drawing the line that connects them, m = s(mp,mq)")
    add_line(figure, mp, mq, "purple", "m")
    add_point(figure, mp, "cyan", "mp")
    add_point(figure, mq, "yellow", "mq")


def show_angles(p_list, q_list, medians, angles, figure):
    # figure = go.Figure()
    # add_vertices(figure, p_list, "green", "P'")
    # add_vertices(figure, q_list, "red", "Q'")
    # add_line(figure, medians[0], medians[1], "purple", "m")

    prev_mp, next_mp = get_neighbour_vertices(p_list)
    prev_mq, next_mq = get_neighbour_vertices(q_list)

    selected_vertices_p = get_selected_vertices(p_list, prev_mp, next_mp)
    add_vertices(figure, selected_vertices_p, "cyan", "ei-1,mp,ei")
    if angles[0] != 0:
        figure.add_annotation(go.layout.Annotation(x=medians[0][0] + 0.15, y=medians[0][1] + 0.15,
                                                   text="a''", showarrow=False))
    if angles[1] != 0:
        figure.add_annotation(go.layout.Annotation(x=medians[0][0] + 0.15, y=medians[0][1] - 0.05,
                                                   text="a'", showarrow=False))

    selected_vertices_q = get_selected_vertices(q_list, prev_mq, next_mq)
    add_vertices(figure, selected_vertices_q, "yellow", "fj-1,mq,fj")
    if angles[2] != 0:
        figure.add_annotation(go.layout.Annotation(x=medians[1][0] - 0.15, y=medians[1][1] + 0.15,
                                                   text="b''", showarrow=False))
    if angles[3] != 0:
        figure.add_annotation(go.layout.Annotation(x=medians[1][0] - 0.15, y=medians[1][1] - 0.15,
                                                   text="b'", showarrow=False))

    st.plotly_chart(figure)

    st.write(f"a'' = {angles[0]}")
    st.write(f"a' = {angles[1]}")
    st.write(f"b'' = {angles[2]}")
    st.write(f"b' = {angles[3]}")

def binary_elimination(p_list, q_list):
    p1, p2 = p_list[0], p_list[-1]
    q1, q2 = q_list[-1], q_list[0]

    mp = p_list[len(p_list) // 2]
    mq = q_list[len(q_list) // 2]

    prev_mp, next_mp = get_neighbour_vertices(p_list)
    prev_mq, next_mq = get_neighbour_vertices(q_list)

    a_up = get_angle(next_mp, mp, mq)
    a_down = get_angle(prev_mp, mp, mq)
    b_up = get_angle(prev_mq, mq, mp)
    b_down = get_angle(next_mq, mq, mp)
    angles = [a_up, a_down, b_up, b_down]
    medians = [mp, mq]

    return angles, medians
    # show_medians(mp, mq, figure)

    # show_angles(p_list, q_list, medians, angles, figure)

    # check_cases1(p_list, q_list, medians, angles)


def handle_page(p_list, q_list):
    show_main_figure(p_list, q_list)
    angles, medians = binary_elimination(p_list, q_list)
