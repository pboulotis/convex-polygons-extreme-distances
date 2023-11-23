import math
import numpy as np
import streamlit as st
from shapely.geometry import Point, LineString


def euclidean_distance(a, b):
    return math.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)


#  If this is >0 then a,b,c are counterclockwise
def calculate_triangle_area(a, b, c):
    return 0.5 * (a[0] * b[1] - a[1] * b[0] + a[1] * c[0] - a[0] * c[1] + b[0] * c[1] - b[1] * c[0])


def convert_counterclockwise(vertices):
    for i in range(len(vertices) - 2):
        if calculate_triangle_area(vertices[i], vertices[i + 1], vertices[i + 2]) < 0:
            return [vertices[0]] + vertices[1:][::-1]
    return vertices


def cross_product(a, b, c):
    ab = (b[0] - a[0], b[1] - a[1])
    bc = (c[0] - b[0], c[1] - b[1])
    return ab[0] * bc[1] - ab[1] * bc[0]


def check_convex_polygon(vertices):
    for i in range(len(vertices)):
        a = vertices[i]
        b = vertices[(i + 1) % len(vertices)]
        c = vertices[(i + 2) % len(vertices)]

        if cross_product(a, b, c) < 0:
            return False
    return True


def polygon_position(polygon1, polygon2):
    mean1 = np.mean(polygon1, axis=0)
    mean2 = np.mean(polygon2, axis=0)

    if mean2[0] > mean1[0]:
        return 'left', 'right'
    return 'right', 'left'


def closest_vertex(vertices, point):
    temp_distance = euclidean_distance(vertices[0], point)
    closest = vertices[0]
    for i in range(1, len(vertices)):
        if euclidean_distance(vertices[i], point) < temp_distance:
            closest = vertices[i]
            temp_distance = euclidean_distance(vertices[i], point)

    return closest


def get_polygon_edges(polygon):
    edges = []
    for i in range(len(polygon)):
        p1 = polygon[i]
        p2 = polygon[(i + 1) % len(polygon)]
        edges.append(LineString([Point(p1), Point(p2)]))
    return edges


def line_equation(point, vertex, test_point):
    px, py = point
    qx, qy = vertex
    x, y = test_point

    return x * (py - qy) - y * (px - qx) + px * qy - py * qx


def find_tangents(polygon, point, u_w_flag):
    tangents = [None, None]

    for vertex in polygon:
        lower_num = 0
        upper_num = 0
        for other_vertex in polygon:
            if vertex == other_vertex:
                continue
            res = line_equation(point, vertex, other_vertex)
            if res <= 0:
                lower_num = lower_num + 1
            else:
                upper_num = upper_num + 1

        if lower_num == len(polygon) - 1:
            if tangents[0] and tangents[0][1] < vertex[1]:
                continue
            tangents[0] = vertex
        if upper_num == len(polygon) - 1:
            if tangents[1] and tangents[0][1] > vertex[1]:
                continue
            tangents[1] = vertex

    if tangents[0][1] > tangents[1][1]:
        return tangents[1], tangents[0]

    return tangents


def get_selected_vertices(vertices, start, end):
    start_idx = vertices.index(start)
    end_idx = vertices.index(end)

    if start_idx < end_idx:
        return vertices[start_idx:end_idx + 1]

    return vertices[start_idx:] + vertices[:end_idx + 1]
