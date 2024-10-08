import streamlit as st
import plotly.graph_objs as go
from polygon_handling import get_polygon_vertices, visualise_polygons, draw_point, draw_line, draw_vertices, \
    intersection_exists, get_selected_vertices, internal_polygon_exists
from geometry_utils import find_tangents

p_list, q_list = None, None


def get_p_q_lists():
    global p_list, q_list
    return p_list, q_list


def set_p_q_lists(p, q):
    global p_list, q_list
    p_list, q_list = p, q


def change_u_w(polygon_p, polygon_q):
    u = None
    w = None
    selected_u_vertex = st.selectbox("Select an u vertex from P polygon", polygon_p,
                                     format_func=lambda vertex: f"({vertex[0]}, {vertex[1]})")
    if selected_u_vertex != u:
        u = selected_u_vertex

    selected_w_vertex = st.selectbox("Select an w vertex from Q polygon", polygon_q,
                                     format_func=lambda vertex: f"({vertex[0]}, {vertex[1]})")
    if selected_w_vertex != w:
        w = selected_w_vertex

    return u, w


def show_u_w_points(u, w):
    figure = visualise_polygons()
    draw_point(figure, u, "green", "u")
    draw_point(figure, w, "red", "w")
    st.plotly_chart(figure, use_container_width=True)


def show_u_tangents(u, polygon_q):
    figure = visualise_polygons()
    w_lower, w_upper = find_tangents(polygon_q, u)
    st.write("We compute the two lines V' and V'' that pass through u and are tangent to Q. "
             "Now w' and w'' are the vertices closest to u where V' and V'' touch Q")
    draw_point(figure, u, "green", "u")
    draw_line(figure, u, w_lower, "green", "V'")
    figure.add_annotation(go.layout.Annotation(x=w_lower[0], y=w_lower[1], text="w'"))
    draw_line(figure, u, w_upper, "purple", "V''")

    figure.add_annotation(go.layout.Annotation(x=w_upper[0], y=w_upper[1], text="w''"))

    st.plotly_chart(figure, use_container_width=True)

    return w_lower, w_upper


def show_w_tangents(w, polygon_p, w_lower, w_upper):
    figure = visualise_polygons()
    u_lower, u_upper = find_tangents(polygon_p, w)
    st.write("We compute the two lines W' and W'' that pass through w and are tangent to P. "
             "Now u' and u'' are the vertices closest to w where W' and W'' touch P")
    draw_point(figure, w, "red", "w")
    figure.add_annotation(go.layout.Annotation(x=w_lower[0], y=w_lower[1], text="w'"))
    figure.add_annotation(go.layout.Annotation(x=w_upper[0], y=w_upper[1], text="w''"))
    draw_line(figure, w, u_lower, "green", "W'")
    figure.add_annotation(go.layout.Annotation(x=u_lower[0], y=u_lower[1], text="u'"))
    draw_line(figure, w, u_upper, "purple", "W''")
    figure.add_annotation(go.layout.Annotation(x=u_upper[0], y=u_upper[1], text="u''"))

    st.plotly_chart(figure, use_container_width=True)

    return u_lower, u_upper


def show_p_q_lists(p, q):
    figure = visualise_polygons()

    figure.add_annotation(go.layout.Annotation(x=q[0][0], y=q[0][1], text="w''"))
    figure.add_annotation(go.layout.Annotation(x=q[-1][0], y=q[-1][1], text="w'"))
    figure.add_annotation(go.layout.Annotation(x=p[-1][0], y=p[-1][1], text="u''"))
    figure.add_annotation(go.layout.Annotation(x=p[0][0], y=p[0][1], text="u'"))

    draw_vertices(figure, p, "green", "P'")
    draw_vertices(figure, q, "red", "Q'")

    st.plotly_chart(figure, use_container_width=True)
    return figure


def show_initial_phase_page(sidebar=False):
    global p_list, q_list
    st.subheader("Initial Phase")
    if intersection_exists() or internal_polygon_exists():
        return
    polygon_p, polygon_q = get_polygon_vertices("P"), get_polygon_vertices("Q")

    if not polygon_p or not polygon_q:
        st.warning("Please fill the vertices first using the 'Polygon coordinates' tab or by selecting an example on "
                   "the 'Home' tab")
        return

    st.write("We choose u and w, as arbitrary vertices in P and Q, respectively")
    u, w = polygon_p[0], polygon_q[-1]
    if sidebar:
        st.write("You will get the correct result for any vertices selected")
        u, w = change_u_w(polygon_p, polygon_q)
    show_u_w_points(u, w)
    w_lower, w_upper = show_u_tangents(u, polygon_q)
    u_lower, u_upper = show_w_tangents(w, polygon_p, w_lower, w_upper)
    p_list = get_selected_vertices(polygon_p, u_lower, u_upper)
    q_list = get_selected_vertices(polygon_q, w_upper, w_lower)
    st.write("We choose the sequences from u' to u'' as P' and from w'' to w' as Q'")
    show_p_q_lists(p_list, q_list)


def get_initial_phase_result_no_display(polygon_p, polygon_q):
    global p_list, q_list
    u = polygon_p[0]
    w = polygon_q[-1]
    w_lower, w_upper = find_tangents(polygon_q, u)
    u_lower, u_upper = find_tangents(polygon_p, w)
    p_list = get_selected_vertices(polygon_p, u_lower, u_upper)
    q_list = get_selected_vertices(polygon_q, w_upper, w_lower)

    return p_list, q_list
