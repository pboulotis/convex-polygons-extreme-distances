import streamlit as st
import numpy as np
# import plotly.graph_objs as go
from polygon_handling import get_polygon_vertices, visualise_polygons, draw_point, draw_vertices
from utils import calculate_triangle_area as area, euclidean_distance


def show_points(i, j):
    figure = visualise_polygons()
    draw_point(figure, i, "cyan", "i")
    draw_point(figure, j, "red", "j")
    st.plotly_chart(figure)


def add_pair2(pair, pair_list, max_distance):
    distance = euclidean_distance(pair[0], pair[1])
    if distance > max_distance:
        pair_list.append(pair)
        max_distance = distance
    return max_distance


def add_pair(pair, pair_list):
    if pair not in pair_list:
        pair_list.append(pair)


def next_index(index, polygon):
    if index + 1 == len(polygon):
        return 0
    return index + 1


def get_antipodal_pairs(p, q):
    pair_list = []
    i = -1
    i0 = len(p) - 1
    j = len(q) - 1

    # st.write(area(p[i], p[next_index(i, p)], q[next_index(j, q)]), area(p[i], p[next_index(i, p)], q[j]))
    while area(p[-1], p[0], q[next_index(j, q)]) > area(p[-1], p[0], q[j]):
        j = next_index(j, q)
    j0 = j

    while j != 0:
        i = next_index(i, p)
        add_pair([p[i], q[j]], pair_list)
        # st.write(f"i: {i} and j: {j}, i0: {i0}")
        # show_points(p[i], q[j])
        # st.write(area(p[i], p[next_index(i, p)], q[next_index(j, q)]), area(p[i], p[next_index(i, p)], q[j]))

        while area(p[i], p[next_index(i, p)], q[next_index(j, q)]) > area(p[i], p[next_index(i, p)], q[j]):
            j = next_index(j, q)
            # st.write(f"New j: {j}")

            # if (i, j) != (j0, i0):
            add_pair([p[i], q[j]], pair_list)

        if area(p[i], p[next_index(i, p)], q[next_index(j, q)]) == area(p[i], p[next_index(i, p)], q[j]):
            # if (i, j) != (j0, i0):

            add_pair([p[i], q[j]], pair_list)
            # st.write(f"New j: {j}")

        if i == i0 and j == j0:
            # st.subheader(f"HERE j = {j}")
            j = next_index(j, q)
    return pair_list


def get_antipodal_pairs_single(polygon):
    pair_list = []
    pn = len(polygon) - 1
    p = pn
    q = next_index(p, polygon)
    while (area(polygon[p], polygon[next_index(p, polygon)], polygon[next_index(q, polygon)]) >
           area(polygon[p], polygon[next_index(p, polygon)], polygon[q])):
        q = next_index(q, polygon)
    q0 = q
    while q != 0:
        p = next_index(p, polygon)
        add_pair([p, q], pair_list)

        while (area(polygon[p], polygon[next_index(p, polygon)], polygon[next_index(q, polygon)]) >
               area(polygon[p], polygon[next_index(p, polygon)], polygon[q])):
            q = next_index(q, polygon)
            if (p, q) != (q0, 0):
                add_pair([p, q], pair_list)

        if (area(polygon[p], polygon[next_index(p, polygon)], polygon[next_index(q, polygon)]) ==
                area(polygon[p], polygon[next_index(p, polygon)], polygon[q])):
            if (p, q) != (q0, pn):
                add_pair([p, q], pair_list)

    return pair_list


def find_max_distance(pair_list):
    max_distance = 0
    vertex_pair = None
    for pair in pair_list:
        temp_distance = euclidean_distance(pair[0], pair[1])
        if temp_distance > max_distance:
            max_distance = temp_distance
            vertex_pair = pair

    return vertex_pair, max_distance


def get_all_pairs(polygon, other_polygon):
    pair_list = []
    for vertex in polygon:
        for other_vertex in other_polygon:
            pair_list.append([vertex, other_vertex])

    return pair_list


def display_pairs(pair_list, label1, label2):
    for pair in range(len(pair_list)):
        st.write(f"{pair + 1})")
        figure = visualise_polygons()
        draw_point(figure, pair_list[pair][0], "cyan", f"Polygon {label1} vertex")
        draw_point(figure, pair_list[pair][1], "red", f"Polygon {label2} vertex")
        st.plotly_chart(figure)


def show_max_distance_result(pairs):
    st.subheader("Maximum distance between the two convex polygons")
    vertex_pair, max_distance = find_max_distance(pairs)
    st.write(f"The maximum distance is {np.round(max_distance, 2)} by the points"
             f" {vertex_pair[0]} and {vertex_pair[1]}")
    figure = visualise_polygons()
    draw_vertices(figure, vertex_pair, "red", "maximum distance")
    st.plotly_chart(figure)


def show_max_dist_page(display=True):
    polygon_p, polygon_q = get_polygon_vertices("P"), get_polygon_vertices("Q")
    if not polygon_p or not polygon_q:
        st.warning("Please fill the polygon vertices first")
        return

    pair_list1 = get_antipodal_pairs(polygon_p, polygon_q)
    pair_list2 = get_antipodal_pairs(polygon_q, polygon_p)

    if display:
        st.write("We need to calculate all the antipodal pairs of the two polygons:")
        st.write("The antipodal pairs from polygon P to Q:")
        display_pairs(pair_list1, "P", "Q")
        st.write("The antipodal pairs from polygon Q to P:")
        display_pairs(pair_list2, "Q", "P")
    pair_list = pair_list1 + pair_list2
    show_max_distance_result(pair_list)

    # TODO REMOVE IN FINAL VERSION
    st.write("---")
    st.write("Higher complexity result:")
    pair_list = get_all_pairs(polygon_p, polygon_q)
    show_max_distance_result(pair_list)
    # TILL HERE
