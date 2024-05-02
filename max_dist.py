import streamlit as st
import numpy as np
# import plotly.graph_objs as go
from polygon_handling import get_polygon_vertices, visualise_polygons, add_point, update_vertices, add_vertices
from utils import calculate_triangle_area as area, euclidean_distance


def add_pair(pair, pair_list):
    if pair not in pair_list:
        pair_list.append(pair)


def next_index(index, polygon):
    if index + 1 == len(polygon):
        return 0
    return index + 1


def get_antipodal_pairs(polygon, other):
    pairs = []
    p = polygon
    q = other
    i = -1
    # i0 = 0
    j = -1

    # st.write(area(p[-1], p[0], q[j + 1]), area(p[-1], p[0], q[j]))
    while area(p[-1], p[0], q[j + 1]) > area(p[-1], p[0], q[j]):
        j = j + 1
    # q0 = q[j]

    while q[j] != q[0]:
        i = next_index(i, p)
        add_pair([p[i], q[j]], pairs)
        # st.write(area(p[i], p[next_index(i, p)], q[next_index(j, q)]), area(p[i], p[next_index(i, p)], q[j]))

        while area(p[i], p[next_index(i, p)], q[next_index(j, q)]) > area(p[i], p[next_index(i, p)], q[j]):
            j = next_index(j, q)
            # if (i, j) != (j0, i0):
            add_pair([p[i], q[j]], pairs)

        if area(p[i], p[next_index(i, p)], q[next_index(j, q)]) == area(p[i], p[next_index(i, p)], q[j]):
            # if (i, j) != (j0, i0):
            #    pairs.append([p[i], q[j]])
            # else:
            add_pair([p[i], q[j]], pairs)

    return pairs


def find_max_distance(pairs):
    max_distance = 0
    vertex_pair = None
    for pair in pairs:
        temp_distance = euclidean_distance(pair[0], pair[1])
        if temp_distance > max_distance:
            max_distance = temp_distance
            vertex_pair = pair

    return vertex_pair, max_distance


def get_all_pairs(polygon, other_polygon):
    pairs = []
    for vertex in polygon:
        for other_vertex in other_polygon:
            pairs.append([vertex, other_vertex])

    return pairs


def display_pairs(pair_list):
    for pair in range(len(pair_list)):
        st.write(f"{pair + 1})")
        figure = visualise_polygons()
        add_point(figure, pair_list[pair][0], "cyan", "Polygon P vertex")
        add_point(figure, pair_list[pair][1], "red", "Polygon Q vertex")
        st.plotly_chart(figure)


def show_max_distance_result(pairs):
    st.subheader("Maximum distance between the two convex polygons")
    vertex_pair, max_distance = find_max_distance(pairs)
    st.write(f"The maximum distance is {np.round(max_distance, 2)} by the points {vertex_pair[0]} and {vertex_pair[1]}")
    figure = visualise_polygons()
    add_vertices(figure, vertex_pair, "red", "maximum distance")
    st.plotly_chart(figure)


def show_max_dist_page(display=True):

    # TODO REMOVE IN FINAL VERSION
    polygon_p = [(0, 0), (0.5, 0), (1, 0.5), (0.5, 1), (0, 1), (-0.5, 0.5)]
    polygon_q = [(2.25, 1.5), (2.5, 2.5), (1.75, 3), (1, 2.5), (1.25, 1.5)]
    update_vertices(polygon_p, "P")
    update_vertices(polygon_q, "Q")
    # TILL HERE

    polygon_p, polygon_q = get_polygon_vertices("P"), get_polygon_vertices("Q")
    if not polygon_p or not polygon_q:
        st.warning("Please fill the polygon vertices first")
        return

    pairs1 = get_antipodal_pairs(polygon_p, polygon_q)
    pairs2 = get_antipodal_pairs(polygon_q, polygon_p)

    if display:
        st.write("We need to calculate all the antipodal pairs of the two polygons:")
        st.write("The antipodal pairs from polygon P to Q:")
        display_pairs(pairs1)
        st.write("The antipodal pairs from polygon Q to P:")
        display_pairs(pairs2)
    pairs = pairs1 + pairs2
    show_max_distance_result(pairs)

    # TODO REMOVE IN FINAL VERSION
    st.write("--------------------------------------------------------------------------------")
    st.write("Higher complexity result:")
    pairs = get_all_pairs(polygon_p, polygon_q)
    show_max_distance_result(pairs)
    # TILL HERE
