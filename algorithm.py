import plotly.graph_objs as go
import streamlit as st

from start import add_point


def show_medians(mp, mq, figure):
    add_point(figure, mp, "cyan", "mp")
    add_point(figure, mq, "yellow", "mq")

    figure.add_trace(go.Scatter(x=[mp[0], mq[0]], y=[mp[1], mq[1]], mode='lines', marker=dict(size=10),
                                line=dict(color='purple'), name="m"))
    st.plotly_chart(figure)


def get_neighbour_vertices(vertices):
    index = len(vertices) // 2
    if index + 1 == len(vertices):
        return vertices[index - 1], vertices[0]
    return vertices[index - 1], vertices[index + 1]


def binary_elimination(p_list, q_list, figure):
    p1, p2 = p_list[0], p_list[-1]
    q1, q2 = q_list[-1], q_list[0]
    mp = p_list[len(p_list) // 2]
    mq = q_list[len(q_list) // 2]
    st.write("We compute the median mp in the P' list as well as the median mq in the Q' list. ")
    st.write("We then compute the line that connects them, m = s(mp,mq)")
    show_medians(mp, mq, figure)
    prev_mp, next_mp = get_neighbour_vertices(p_list)
