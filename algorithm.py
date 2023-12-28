import streamlit as st
import plotly.graph_objs as go
import cases
from start import add_point, add_line, add_vertices, visualize_polygons
from utils import get_neighbour_vertices, get_selected_vertices, get_angle


def get_main_figure(p_list, q_list, annotations=True):
    figure = visualize_polygons()

    add_vertices(figure, p_list, "green", "P'")
    add_vertices(figure, q_list, "red", "Q'")

    if annotations:
        figure.add_annotation(go.layout.Annotation(x=p_list[0][0], y=p_list[0][1], text="p1"))
        figure.add_annotation(go.layout.Annotation(x=p_list[-1][0], y=p_list[-1][1], text="p2"))
        figure.add_annotation(go.layout.Annotation(x=q_list[0][0], y=q_list[0][1], text="q2"))
        figure.add_annotation(go.layout.Annotation(x=q_list[-1][0], y=q_list[-1][1], text="q1"))

    return figure


def show_medians(p_list, q_list, figure):
    mp = p_list[len(p_list) // 2]
    mq = q_list[len(q_list) // 2]

    st.write("We compute the median mp in the P' list as well as the median mq in the Q' list."
             " Thus drawing the line that connects them, m = s(mp,mq)")
    add_line(figure, mp, mq, "purple", "m")
    add_point(figure, mp, "yellow", "mp")
    add_point(figure, mq, "cyan", "mq")
    st.plotly_chart(figure)


def show_angles(p_list, q_list, medians, angles):
    figure = get_main_figure(p_list, q_list, annotations=False)
    add_line(figure, medians[0], medians[1], "purple", "m")

    st.write("In order to execute the binary elimination algorithm, we will need to calculate the angles created from "
             "the m line that connects the median vertices as well as the edges with their neighbour vertices.")
    st.write("More specifically, ei-1 and ei are the edges with the previous and next neighbouring vertices of mp."
             "Likewise the fj-1 and fj are the edges with the previous and next neighbouring vertices of mq.")
    st.write("Now we distinguish the following angles:")
    st.write("α' the angle from ei-1 to m and α'' the angle from m to ei")
    st.write("β' the angle from m to fj and β'' the angle from fj-1 to m")
    prev_mp, next_mp = get_neighbour_vertices(p_list)
    prev_mq, next_mq = get_neighbour_vertices(q_list)

    selected_vertices_p = get_selected_vertices(p_list, prev_mp, next_mp)
    add_vertices(figure, selected_vertices_p, "yellow", "ei-1,mp,ei")

    if angles[0] != 0:
        figure.add_annotation(go.layout.Annotation(x=medians[0][0] + 0.05, y=medians[0][1] + 0.15,
                                                   text="α''", arrowcolor="red"))
    if angles[1] != 0:
        figure.add_annotation(go.layout.Annotation(x=medians[0][0] + 0.15, y=medians[0][1] - 0.05,
                                                   text="α'", arrowcolor="red", ax=20, ay=20))

    selected_vertices_q = get_selected_vertices(q_list, prev_mq, next_mq)
    add_vertices(figure, selected_vertices_q, "cyan", "fj-1,mq,fj")

    if angles[2] != 0:
        figure.add_annotation(go.layout.Annotation(x=medians[1][0] - 0.15, y=medians[1][1] + 0.05,
                                                   text="β''", arrowcolor="red", ax=-30, ay=10))
    if angles[3] != 0:
        figure.add_annotation(go.layout.Annotation(x=medians[1][0] - 0.15, y=medians[1][1] - 0.15,
                                                   text="β'", arrowcolor="red", ax=-30, ay=20))

    st.image('angles_example.jpg', caption="An example of the angles on two polygons")
    st.plotly_chart(figure)

    st.write(f"Angle values: α'' = {angles[0]},  α' = {angles[1]},  β'' = {angles[2]},  β' = {angles[3]}")


def compute_angles_medians(p_list, q_list):
    # p1, p2 = p_list[0], p_list[-1]
    # q1, q2 = q_list[-1], q_list[0]

    mp = p_list[len(p_list) // 2]
    mq = q_list[len(q_list) // 2]

    prev_mp, next_mp = get_neighbour_vertices(p_list)
    prev_mq, next_mq = get_neighbour_vertices(q_list)

    a_up = get_angle(mq, mp, next_mp)
    a_down = get_angle(prev_mp, mp, mq)
    b_up = get_angle(mp, mq, prev_mq)
    b_down = get_angle(mp, mq, next_mq)
    angles = [a_up, a_down, b_up, b_down]
    medians = [mp, mq]

    return angles, medians


def binary_elimination(p_list, q_list):
    iteration = 1
    while iteration < 4:
        st.subheader(f"Iteration {iteration}:")
        angles, medians = (compute_angles_medians(p_list, q_list))
        st.write(f"angles:{angles}")
        p_list, q_list = cases.check_cases1(p_list, q_list, medians, angles)
        p_list, q_list = cases.check_cases2(p_list, q_list, medians, angles)
        p_list, q_list = cases.check_cases3(p_list, q_list, medians, angles)
        iteration = iteration + 1
    if len(p_list) < 2 and len(q_list) < 2:
        st.info("You can now go to the Final Phase page")


def handle_page(p_list, q_list):
    figure = get_main_figure(p_list, q_list)
    show_medians(p_list, q_list, figure)
    angles, medians = compute_angles_medians(p_list, q_list)
    show_angles(p_list, q_list, medians, angles)

    st.write("Based on the number of vertices on the P' and Q' sequences as well as the values of the angles,"
             "each iteration we have the following cases:")
    st.write("Case 1: One of the sequences contains only one vertex")
    st.write("Case 2: One of the sequences contains only two vertices")
    st.write("Case 3: Both sequences contain at least three vertices each")

    binary_elimination(p_list, q_list)
