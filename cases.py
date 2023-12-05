import streamlit as st
from algorithm import show_main_figure
from utils import get_selected_vertices


def show_case1_p(q_list, mq, angles):
    st.write("P' contains only one vertex, changing the Q' sequence ")
    st.write(f"b'' = {angles[2]}")
    st.write(f"b' = {angles[3]}")
    if angles[2] >= 90:
        q_list = get_selected_vertices(q_list, mq, q_list[-1])
    if angles[3] >= 90:
        q_list = get_selected_vertices(q_list, q_list[0], mq)
    return q_list


def show_case1_q(p_list, mp, angles):
    st.write("Q' contains only one vertex, changing the P' sequence")
    if angles[0] >= 90:
        p_list = get_selected_vertices(p_list, mp, p_list[-1])
    if angles[1] >= 90:
        p_list = get_selected_vertices(p_list, p_list[0], mp)
    return p_list


def check_cases1(p_list, q_list, medians, angles):
    st.subheader("Case 1:")
    if len(p_list) == 1:
        q_list = show_case1_p(q_list, medians[1], angles)
        show_main_figure(p_list, q_list)
    elif len(q_list) == 1:
        p_list = show_case1_q(p_list, medians[0], angles)
        show_main_figure(p_list, q_list)
    else:
        st.write("Not satisfied")
    return p_list, q_list