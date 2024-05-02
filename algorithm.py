import streamlit as st
import plotly.graph_objs as go
from cases import check_cases, check_cases_no_display
from polygon_handling import add_point, add_line, add_vertices, visualise_polygons
from utils import get_neighbour_vertices, get_angle


def get_main_figure(p_list, q_list, annotations=True):
    figure = visualise_polygons()

    add_vertices(figure, p_list, "green", "P'")
    add_vertices(figure, q_list, "red", "Q'")

    if annotations:
        figure.add_annotation(go.layout.Annotation(x=p_list[0][0], y=p_list[0][1], text="p₁"))
        figure.add_annotation(go.layout.Annotation(x=p_list[-1][0], y=p_list[-1][1], text="p₂"))
        figure.add_annotation(go.layout.Annotation(x=q_list[0][0], y=q_list[0][1], text="q₂"))
        figure.add_annotation(go.layout.Annotation(x=q_list[-1][0], y=q_list[-1][1], text="q₁"))

    return figure


def show_medians(p_list, q_list, figure):
    mp = p_list[len(p_list) // 2]
    mq = q_list[len(q_list) // 2]

    st.write("We compute the median mₚ in the P' list as well as the median m₍q₎ in the Q' list."
             " Thus drawing the line that connects them, m = s(mₚ,m₍q₎)")
    add_line(figure, mp, mq, "purple", "m")
    add_point(figure, mp, "yellow", "mₚ")
    add_point(figure, mq, "cyan", "m₍q₎")
    st.plotly_chart(figure)


def show_angle_example():
    st.write("In order to execute the binary elimination algorithm, we will need to calculate the angles created from "
             "the m line that connects the median vertices as well as the edges with their neighbour vertices.")
    st.write("More specifically, eᵢ₋₁ and eᵢ are the edges with the previous and next neighbouring vertices of mₚ."
             "Likewise the fⱼ₋₁ and fⱼ are the edges with the previous and next neighbouring vertices of m₍q₎.")
    st.write("Now we distinguish the following angles:")
    st.write("α' the angle from eᵢ₋₁ to m and α'' the angle from m to eᵢ")
    st.write("β' the angle from m to fⱼ and β'' the angle from fⱼ₋₁ to m")

    st.image('angles_example.jpg', caption="An example of the angles on two polygons")


def compute_angles_medians(p_list, q_list):
    mp = p_list[len(p_list) // 2]
    mq = q_list[len(q_list) // 2]

    prev_mp, next_mp = get_neighbour_vertices(p_list, mp)
    prev_mq, next_mq = get_neighbour_vertices(q_list, mq)

    a_up = get_angle(mq, mp, next_mp)
    a_down = get_angle(prev_mp, mp, mq)
    b_up = get_angle(mp, mq, prev_mq)
    b_down = get_angle(mp, mq, next_mq)
    angles = [a_up, a_down, b_up, b_down]
    medians = [mp, mq]

    return angles, medians


def binary_elimination(p_list, q_list):
    iteration = 1
    while len(p_list) > 2 or len(q_list) > 2:
        st.subheader(f"Iteration {iteration}:")
        angles, medians = (compute_angles_medians(p_list, q_list))
        st.write(f"Angle values: α'' = {angles[0]},  α' = {angles[1]},  β'' = {angles[2]},  β' = {angles[3]}")
        p_list, q_list = check_cases(p_list, q_list, medians, angles)
        iteration = iteration + 1
    # st.info("You can now go to the Final Phase page")
    return p_list, q_list


def handle_algorithm_page(p_list, q_list):
    figure = get_main_figure(p_list, q_list)
    show_medians(p_list, q_list, figure)
    show_angle_example()

    st.write("Based on the number of vertices on the P' and Q' sequences, "
             "we have the following cases for each iteration:")
    st.write("Case 1: One of the sequences contains only one vertex")
    st.write("Case 2: One of the sequences contains only two vertices")
    st.write("Case 3: Both sequences contain at least three vertices each")

    return binary_elimination(p_list, q_list)


def binary_elimination_no_display(p_list, q_list):
    iteration = 1
    while len(p_list) > 2 or len(q_list) > 2:
        angles, medians = (compute_angles_medians(p_list, q_list))
        p_list, q_list = check_cases_no_display(p_list, q_list, medians, angles)
        iteration = iteration + 1

    return p_list, q_list
