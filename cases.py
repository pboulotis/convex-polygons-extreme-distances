import streamlit as st
import plotly.graph_objs as go
from start import add_vertices, visualize_polygons, add_line, add_point
from utils import get_selected_vertices


def show_figure(p_list, q_list):
    figure = visualize_polygons()

    add_vertices(figure, p_list, "green", "P'")
    add_vertices(figure, q_list, "red", "Q'")

    if len(p_list) == 1:
        figure.add_annotation(go.layout.Annotation(x=p_list[0][0], y=p_list[0][1], text="p1 = p2"))
    else:
        figure.add_annotation(go.layout.Annotation(x=p_list[0][0], y=p_list[0][1], text="p1"))
        figure.add_annotation(go.layout.Annotation(x=p_list[-1][0], y=p_list[-1][1], text="p2"))

    if len(q_list) == 1:
        figure.add_annotation(go.layout.Annotation(x=q_list[0][0], y=q_list[0][1], text="q2 = q1"))
    else:
        figure.add_annotation(go.layout.Annotation(x=q_list[0][0], y=q_list[0][1], text="q2"))
        figure.add_annotation(go.layout.Annotation(x=q_list[-1][0], y=q_list[-1][1], text="q1"))

    mp = p_list[len(p_list) // 2]
    mq = q_list[len(q_list) // 2]

    add_line(figure, mp, mq, "purple", "m")
    add_point(figure, mp, "yellow", "mp")
    add_point(figure, mq, "cyan", "mq")
    st.plotly_chart(figure)


def show_case1_p(q_list, mq, angles):
    st.write("Case 1: P' contains only one vertex, changing the Q' sequence ")
    st.write(f"b'' = {angles[2]}")
    st.write(f"b' = {angles[3]}")
    if angles[2] >= 90:
        q_list = get_selected_vertices(q_list, mq, q_list[-1])
    if angles[3] >= 90:
        q_list = get_selected_vertices(q_list, q_list[0], mq)
    return q_list


def show_case1_q(p_list, mp, angles):
    st.write("Case 1: Q' contains only one vertex, changing the P' sequence")
    if angles[0] >= 90:
        p_list = get_selected_vertices(p_list, mp, p_list[-1])
    if angles[1] >= 90:
        p_list = get_selected_vertices(p_list, p_list[0], mp)
    return p_list


def check_cases1(p_list, q_list, medians, angles):
    if len(p_list) == 1:
        q_list = show_case1_p(q_list, medians[1], angles)
        show_figure(p_list, q_list)
    elif len(q_list) == 1:
        p_list = show_case1_q(p_list, medians[0], angles)
        show_figure(p_list, q_list)
    return p_list, q_list


# TODO
def show_case2_p(q_list, mq, angles):
    st.write("Case 2: P' contains only two vertices")
    return q_list


# TODO
def show_case2_q(p_list, mp, angles):
    st.write("Case 2: Q' contains only two vertices")
    return p_list


def check_cases2(p_list, q_list, medians, angles):
    if len(p_list) == 2:
        q_list = show_case2_p(q_list, medians[1], angles)
        show_figure(p_list, q_list)
    elif len(q_list) == 2:
        p_list = show_case2_q(p_list, medians[0], angles)
        show_figure(p_list, q_list)
    return p_list, q_list


def handle_case3_1(p_list, q_list, medians, angles):
    if angles[1] + angles[3] > 180:
        if angles[1] > 90:
            p_list = get_selected_vertices(p_list, medians[0], p_list[-1])
        if angles[3] > 90:
            q_list = get_selected_vertices(q_list, q_list[0], medians[1])
    if angles[0] + angles[2] > 180:
        if angles[0] > 90:
            p_list = get_selected_vertices(p_list, p_list[0], medians[0])
        if angles[2] >= 90:
            q_list = get_selected_vertices(q_list, medians[1], q_list[-1])

    return p_list, q_list


def handle_case3_2(p_list, q_list, medians, angles):
    if angles[0] <= 0 or angles[0] >= 180:
        p_list = get_selected_vertices(p_list, medians[0], p_list[-1])
    if angles[1] <= 0 or angles[1] >= 180:
        p_list = get_selected_vertices(p_list, p_list[0], medians[0])
    if angles[2] >= 180 or angles[2] <= 0:
        q_list = get_selected_vertices(q_list, medians[1], q_list[-1])
    if angles[3] >= 180 or angles[3] <= 0:
        q_list = get_selected_vertices(q_list, q_list[0], medians[1])

    return p_list, q_list


def check_cases3(p_list, q_list, medians, angles):
    if len(p_list) > 2 and len(q_list) > 2:
        st.write("Case 3")
        if angles[0] > 0 and angles[1] > 0 and angles[2] > 0 and angles[3] > 0:
            p_list, q_list = handle_case3_1(p_list, q_list, medians, angles)

        p_list, q_list = handle_case3_2(p_list, q_list, medians, angles)

        show_figure(p_list, q_list)
    return p_list, q_list
