import streamlit as st
import plotly.graph_objs as go
from start import get_polygon_vertices, visualize_polygons
from utils import find_tangents, get_selected_vertices


def show_u_w(vertices1, vertices2):
    u = None
    w = None
    fig = visualize_polygons()

    selected_u_vertex = st.selectbox("Select a vertex for u", vertices1, format_func=lambda v: f"({v[0]}, {v[1]})")
    if selected_u_vertex != u:
        u = selected_u_vertex

    selected_w_vertex = st.selectbox("Select a vertex for w", vertices2, format_func=lambda v: f"({v[0]}, {v[1]})")
    if selected_w_vertex != w:
        w = selected_w_vertex

    fig.add_trace(go.Scatter(x=[u[0]], y=[u[1]], mode='markers',
                             marker=dict(size=12, color="green"), name="u"))
    fig.add_trace(go.Scatter(x=[w[0]], y=[w[1]], mode='markers',
                             marker=dict(size=12, color="red"), name="w"))
    st.plotly_chart(fig, use_container_width=True)

    return u, w


def show_u_tangents(u, vertices2):
    fig = visualize_polygons()
    w_lower, w_upper = find_tangents(vertices2, u, "u")

    fig.add_trace(go.Scatter(x=[u[0]], y=[u[1]], mode='markers',
                             marker=dict(size=12, color="green"), name="u"))
    fig.add_trace(go.Scatter(x=[u[0], w_lower[0]], y=[u[1], w_lower[1]], mode='lines',
                             line=dict(color='green'), name="V'"))
    fig.add_annotation(go.layout.Annotation(x=w_lower[0], y=w_lower[1], text="w'"))
    fig.add_trace(go.Scatter(x=[u[0], w_upper[0]], y=[u[1], w_upper[1]], mode='lines',
                             line=dict(color='purple'), name="W''"))
    fig.add_annotation(go.layout.Annotation(x=w_upper[0], y=w_upper[1], text="w''"))

    st.plotly_chart(fig, use_container_width=True)

    return w_lower, w_upper


def show_w_tangents(w, vertices1, w_lower, w_upper):
    fig = visualize_polygons()
    u_lower, u_upper = find_tangents(vertices1, w, "w")

    fig.add_trace(go.Scatter(x=[w[0]], y=[w[1]], mode='markers',
                             marker=dict(size=12, color="red"), name="w"))
    fig.add_annotation(go.layout.Annotation(x=w_lower[0], y=w_lower[1], text="w'"))
    fig.add_annotation(go.layout.Annotation(x=w_upper[0], y=w_upper[1], text="w''"))

    fig.add_trace(go.Scatter(x=[w[0], u_lower[0]], y=[w[1], u_lower[1]], mode='lines',
                             line=dict(color='green'), name="W'"))
    fig.add_annotation(go.layout.Annotation(x=u_lower[0], y=u_lower[1], text="u'"))
    fig.add_trace(go.Scatter(x=[w[0], u_upper[0]], y=[w[1], u_upper[1]], mode='lines',
                             line=dict(color='purple'), name="V''"))
    fig.add_annotation(go.layout.Annotation(x=u_upper[0], y=u_upper[1], text="u''"))

    st.plotly_chart(fig, use_container_width=True)

    return u_lower, u_upper


def show_p_q_lists(p_list, q_list):
    fig = visualize_polygons()

    fig.add_annotation(go.layout.Annotation(x=q_list[0][0], y=q_list[0][1], text="w''"))
    fig.add_annotation(go.layout.Annotation(x=q_list[-1][0], y=q_list[-1][1], text="w'"))
    fig.add_annotation(go.layout.Annotation(x=p_list[-1][0], y=p_list[-1][1], text="u''"))
    fig.add_annotation(go.layout.Annotation(x=p_list[0][0], y=p_list[0][1], text="u'"))

    x1, y1 = zip(*p_list)
    fig.add_trace(go.Scatter(x=list(x1), y=list(y1), mode='lines+markers', marker=dict(size=10),
                             line=dict(color='green'), name="P'"))

    x2, y2 = zip(*q_list)
    fig.add_trace(go.Scatter(x=list(x2), y=list(y2), mode='lines+markers', marker=dict(size=10),
                             line=dict(color='red'), name="Q'"))

    st.plotly_chart(fig, use_container_width=True)


def show_initial_phase_page():
    st.title("Initial Phase")
    vertices1, vertices2 = get_polygon_vertices("P"), get_polygon_vertices("Q")

    if not vertices1 or not vertices2:
        st.info("Please fill the vertices first")
    else:
        u, w = show_u_w(vertices1, vertices2)
        w_lower, w_upper = show_u_tangents(u, vertices2)
        u_lower, u_upper = show_w_tangents(w, vertices1, w_lower, w_upper)
        p_list = get_selected_vertices(vertices1, u_lower, u_upper)
        q_list = get_selected_vertices(vertices2, w_upper, w_lower)
        show_p_q_lists(p_list, q_list)
