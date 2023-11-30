import streamlit as st
import plotly.graph_objs as go
from start import get_polygon_vertices, visualize_polygons, add_point, add_line
from utils import find_tangents, get_selected_vertices

p_list, q_list = None, None


def get_p_q_lists():
    global p_list, q_list
    return p_list, q_list


def show_u_w(vertices1, vertices2):
    u = None
    w = None
    figure = visualize_polygons()
    st.write("We choose u and w, as arbitrary points in P and Q, respectively")
    selected_u_vertex = st.selectbox("Select a vertex for u", vertices1, format_func=lambda v: f"({v[0]}, {v[1]})")
    if selected_u_vertex != u:
        u = selected_u_vertex

    selected_w_vertex = st.selectbox("Select a vertex for w", vertices2, format_func=lambda v: f"({v[0]}, {v[1]})")
    if selected_w_vertex != w:
        w = selected_w_vertex

    add_point(figure, u, "green", "u")
    add_point(figure, w, "red", "w")

    st.plotly_chart(figure, use_container_width=True)

    return u, w


def show_u_tangents(u, vertices2):
    figure = visualize_polygons()
    w_lower, w_upper = find_tangents(vertices2, u)
    st.write("We compute the two lines V' and V'' that pass through u and are tangent to Q."
             "Now w' and w'' are the vertices closest to u where V' and V'' touch Q")
    add_point(figure, u, "green", "u")
    add_line(figure, u, w_lower, "green", "V'")
    figure.add_annotation(go.layout.Annotation(x=w_lower[0], y=w_lower[1], text="w'"))
    add_line(figure, u, w_upper, "purple", "V''")

    figure.add_annotation(go.layout.Annotation(x=w_upper[0], y=w_upper[1], text="w''"))

    st.plotly_chart(figure, use_container_width=True)

    return w_lower, w_upper


def show_w_tangents(w, vertices1, w_lower, w_upper):
    figure = visualize_polygons()
    u_lower, u_upper = find_tangents(vertices1, w)
    st.write("We compute the two lines W' and W'' that pass through w and are tangent to P."
             "Now u' and u'' are the vertices closest to w where W' and W'' touch P")
    add_point(figure, w, "red", "w")
    figure.add_annotation(go.layout.Annotation(x=w_lower[0], y=w_lower[1], text="w'"))
    figure.add_annotation(go.layout.Annotation(x=w_upper[0], y=w_upper[1], text="w''"))
    add_line(figure, w, u_lower, "green", "W'")
    figure.add_annotation(go.layout.Annotation(x=u_lower[0], y=u_lower[1], text="u'"))
    add_line(figure, w, u_upper, "purple", "W''")
    figure.add_annotation(go.layout.Annotation(x=u_upper[0], y=u_upper[1], text="u''"))

    st.plotly_chart(figure, use_container_width=True)

    return u_lower, u_upper


def show_p_q_lists(p_list, q_list):
    figure = visualize_polygons()

    figure.add_annotation(go.layout.Annotation(x=q_list[0][0], y=q_list[0][1], text="w''"))
    figure.add_annotation(go.layout.Annotation(x=q_list[-1][0], y=q_list[-1][1], text="w'"))
    figure.add_annotation(go.layout.Annotation(x=p_list[-1][0], y=p_list[-1][1], text="u''"))
    figure.add_annotation(go.layout.Annotation(x=p_list[0][0], y=p_list[0][1], text="u'"))

    x1, y1 = zip(*p_list)
    figure.add_trace(go.Scatter(x=list(x1), y=list(y1), mode='lines+markers', marker=dict(size=10),
                                line=dict(color='green'), name="P'"))

    x2, y2 = zip(*q_list)
    figure.add_trace(go.Scatter(x=list(x2), y=list(y2), mode='lines+markers', marker=dict(size=10),
                                line=dict(color='red'), name="Q'"))

    st.plotly_chart(figure, use_container_width=True)
    return figure


def show_initial_phase_page():
    global p_list, q_list
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
        st.write("We choose the sequences from u' to u'' as P' and from w'' to w' as Q'")
        show_p_q_lists(p_list, q_list)
