import streamlit as st
import plotly.graph_objs as go
from polygon_handling import draw_vertices, visualise_polygons, draw_line, draw_point
from utils import get_selected_vertices, get_orthogonal_projection


def handle_case1_p(q_list, mq, angles):
    if angles[2] >= 90:
        q_list = get_selected_vertices(q_list, q_list[0], mq)
    if angles[3] >= 90:
        q_list = get_selected_vertices(q_list, mq, q_list[-1])

    return q_list


def handle_case1_q(p_list, mp, angles):
    if angles[0] >= 90:
        p_list = get_selected_vertices(p_list, p_list[0], mp)
    if angles[1] >= 90:
        p_list = get_selected_vertices(p_list, mp, p_list[-1])

    return p_list


def handle_case2_p(p_list, q_list, mq, angles):
    if angles[1] >= 0:
        if angles[1] + angles[3] > 180:
            if angles[1] >= 90:
                p_list = [p_list[1]]
            if angles[3] >= 90:
                q_list = get_selected_vertices(q_list, q_list[0], mq)

        if angles[2] >= 90:
            q_list = get_selected_vertices(q_list, mq, q_list[-1])

        if angles[1] < angles[2] < 90:
            if get_orthogonal_projection(p_list[0], p_list[1], mq):
                q_list = get_selected_vertices(q_list, mq, q_list[-1])
            else:
                p_list = [p_list[0]]
    else:
        p_list = [p_list[0]]
        if angles[2] >= 180:
            q_list = get_selected_vertices(q_list, q_list[0], mq)
        if angles[3] >= 180:
            q_list = get_selected_vertices(q_list, mq, q_list[-1])

    return p_list, q_list


def handle_case2_q(p_list, q_list, mp, angles):
    if angles[3] >= 0:
        if angles[1] + angles[3] > 180:
            if angles[3] >= 90:
                q_list = [q_list[1]]
            if angles[1] >= 90:
                p_list = get_selected_vertices(p_list, p_list[0], mp)

        if angles[0] >= 90:
            p_list = get_selected_vertices(p_list, mp, p_list[-1])

        if angles[3] < angles[0] < 90:
            if get_orthogonal_projection(q_list[0], q_list[1], mp):
                p_list = get_selected_vertices(p_list, mp, p_list[-1])
            q_list = [q_list[0]]

    else:
        q_list = [q_list[0]]
        if angles[1] >= 180:
            p_list = get_selected_vertices(p_list, p_list[0], mp)
        if angles[0] >= 180:
            p_list = get_selected_vertices(p_list, mp, p_list[-1])

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


def show_figure(p_list, q_list):
    figure = visualise_polygons()

    draw_vertices(figure, p_list, "green", "P'")
    draw_vertices(figure, q_list, "red", "Q'")

    if len(p_list) == 1:
        figure.add_annotation(go.layout.Annotation(x=p_list[0][0], y=p_list[0][1], text="p₁ = p₂"))
    else:
        figure.add_annotation(go.layout.Annotation(x=p_list[0][0], y=p_list[0][1], text="p₁"))
        figure.add_annotation(go.layout.Annotation(x=p_list[-1][0], y=p_list[-1][1], text="p₂"))

    if len(q_list) == 1:
        figure.add_annotation(go.layout.Annotation(x=q_list[0][0], y=q_list[0][1], text="q₂ = q₁"))
    else:
        figure.add_annotation(go.layout.Annotation(x=q_list[0][0], y=q_list[0][1], text="q₂"))
        figure.add_annotation(go.layout.Annotation(x=q_list[-1][0], y=q_list[-1][1], text="q₁"))

    mp = p_list[len(p_list) // 2]
    mq = q_list[len(q_list) // 2]

    draw_line(figure, mp, mq, "purple", "m")
    draw_point(figure, mp, "blue", "mₚ")
    st.plotly_chart(figure)
    draw_point(figure, mq, "yellow", "m₍q₎")


def check_cases(p_list, q_list, medians, angles):
    if len(p_list) == 1:
        st.write("Case 1: P' contains only one vertex, changing the Q' sequence ")
        q_list = handle_case1_p(q_list, medians[1], angles)
    elif len(q_list) == 1:
        st.write("Case 1: Q' contains only one vertex, changing the P' sequence")
        p_list = handle_case1_q(p_list, medians[0], angles)
    elif len(p_list) == 2:
        st.write("Case 2: P' contains only two vertices")
        p_list, q_list = handle_case2_p(p_list, q_list, medians[1], angles)
    elif len(q_list) == 2:
        st.write("Case 2: Q' contains only two vertices")
        p_list, q_list = handle_case2_q(p_list, q_list, medians[0], angles)
    else:
        st.write("Case 3")
        if angles[0] > 0 and angles[1] > 0 and angles[2] > 0 and angles[3] > 0:
            p_list, q_list = handle_case3_1(p_list, q_list, medians, angles)

        p_list, q_list = handle_case3_2(p_list, q_list, medians, angles)

    show_figure(p_list, q_list)

    return p_list, q_list


def check_cases_no_display(p_list, q_list, medians, angles):
    if len(p_list) == 1:
        q_list = handle_case1_p(q_list, medians[1], angles)
    elif len(q_list) == 1:
        p_list = handle_case1_q(p_list, medians[0], angles)
    elif len(p_list) == 2:
        p_list, q_list = handle_case2_p(p_list, q_list, medians[1], angles)
    elif len(q_list) == 2:
        p_list, q_list = handle_case2_q(p_list, q_list, medians[0], angles)
    else:
        if angles[0] > 0 and angles[1] > 0 and angles[2] > 0 and angles[3] > 0:
            p_list, q_list = handle_case3_1(p_list, q_list, medians, angles)

        p_list, q_list = handle_case3_2(p_list, q_list, medians, angles)

    return p_list, q_list
