import math
import numpy as np
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
    if not vertices:
        return True
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


def find_tangents(polygon, point):
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

    if start == end:
        return [start]

    if start_idx < end_idx:
        return vertices[start_idx:end_idx + 1]

    return vertices[start_idx:] + vertices[:end_idx + 1]


def get_neighbour_vertices(vertices):
    index = len(vertices) // 2
    if index + 1 == len(vertices):
        return vertices[index - 1], vertices[0]
    return vertices[index - 1], vertices[index + 1]


# def calculate_slope(point1, point2):
#     x1, y1 = point1
#     x2, y2 = point2
#     if x2 - x1 == 0:
#         return float('inf')
#     # return sys.maxint
#     return float(y2 - y1) / (x2 - x1)
#
#
# def calculate_angle(point1, point2, point3, point4):
#     m1 = calculate_slope(point1, point2)
#     m2 = calculate_slope(point3, point4)
#
#     angle = abs((m2 - m1) / (1 + m1 * m2))
#     ret = math.atan(angle)
#
#     return (ret * 180) / math.pi


def is_angle_negative(a, b, c):
    ang = math.degrees(math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0]))
    return True if ang < 0 else False


def get_angle(a, b, c):
    if a == b or b == c or a == c:
        return None

    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    ba = a - b
    bc = c - b

    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(cosine_angle)
    angle = np.round(np.degrees(angle), 2)
    if is_angle_negative(a, b, c):
        return angle * (-1)
    return angle
