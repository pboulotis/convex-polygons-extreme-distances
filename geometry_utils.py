import math
import numpy as np
from shapely.geometry import Polygon


def calculate_euclidean_distance(a, b):
    return math.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)


#  If this is >0 then a,b,c are assigned counterclockwise
def area(a, b, c):
    return 0.5 * (a[0] * b[1] - a[1] * b[0] + a[1] * c[0] - a[0] * c[1] + b[0] * c[1] - b[1] * c[0])


def convert_to_counterclockwise(vertices):
    for i in range(len(vertices) - 2):
        if area(vertices[i], vertices[i + 1], vertices[i + 2]) < 0:
            return [vertices[0]] + vertices[1:][::-1]
    return vertices


def cross_product(a, b, c):
    ab = (b[0] - a[0], b[1] - a[1])
    bc = (c[0] - b[0], c[1] - b[1])
    return ab[0] * bc[1] - ab[1] * bc[0]


def is_convex_polygon(vertices):
    if not vertices:
        return True
    for i in range(len(vertices) - 2):
        if cross_product(vertices[i], vertices[i + 1], vertices[i + 2]) < 0:
            return False
    return True


def check_polygon_intersection(polygon_p_list, polygon_q_list):
    polygon_p = Polygon(polygon_p_list)
    polygon_q = Polygon(polygon_q_list)
    intersection = polygon_p.intersection(polygon_q)
    if not intersection:
        return None
    if intersection.geom_type == 'Point':
        # A single intersection point
        return round(intersection.x, 2), round(intersection.y, 2)
    elif intersection.geom_type == 'LineString':
        # Points in the same line
        return [(round(x, 2), round(y, 2)) for x, y in list(intersection.coords)]

    # Multiple intersection points
    all_intersection_points = list(intersection.exterior.coords)
    intersection_points = []
    for vertex in all_intersection_points:
        if vertex in polygon_p_list and vertex in polygon_q_list:
            intersection_points.append([round(vertex[0], 2), round(vertex[1], 2)])
        elif vertex not in polygon_p_list and vertex not in polygon_q_list:
            intersection_points.append([round(vertex[0], 2), round(vertex[1], 2)])
    return intersection_points


def is_polygon_position_correct(polygon_p, polygon_q):
    mean1 = np.mean(polygon_p, axis=0)
    mean2 = np.mean(polygon_q, axis=0)

    if mean2[0] < mean1[0]:
        return False
    return True


def get_neighbour_vertices(polygon, vertex):
    index = polygon.index(vertex)
    if index + 1 == len(polygon):
        return polygon[index - 1], polygon[0]
    return polygon[index - 1], polygon[index + 1]


def calculate_line_equation(point, vertex, test_point):
    px, py = point
    qx, qy = vertex
    x, y = test_point

    return x * (py - qy) - y * (px - qx) + px * qy - py * qx


def find_tangents(polygon, point):
    lower_tangent = None
    upper_tangent = None

    for vertex in polygon:
        neighbour_vertices = get_neighbour_vertices(polygon, vertex)
        res1 = calculate_line_equation(point, vertex, neighbour_vertices[0])
        res2 = calculate_line_equation(point, vertex, neighbour_vertices[1])

        if res1 <= 0 and res2 <= 0:
            if lower_tangent and lower_tangent[1] < vertex[1]:
                continue
            lower_tangent = vertex
        elif res1 >= 0 and res2 >= 0:
            if upper_tangent and upper_tangent[1] > vertex[1]:
                continue
            upper_tangent = vertex

    if not lower_tangent or not upper_tangent:
        # The polygon is inside the other polygon
        return None, None

    if lower_tangent[1] > upper_tangent[1]:
        return upper_tangent, lower_tangent

    return lower_tangent, upper_tangent


def is_angle_negative(a, b, c):
    ang = math.degrees(math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0]))
    return True if ang < 0 else False


def get_angle(a, b, c):
    if a == b or b == c or a == c:
        return 0  

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


def calculate_slope(a, b):
    return (b[1] - a[1]) / (b[0] - a[0])


def calculate_projection_x(a, c, slope, reverse_slope):
    return (c[1] - (reverse_slope * c[0]) - a[1] + (slope * a[0])) / (slope - reverse_slope)


def calculate_projection_y(c, reverse_slope, x):
    return c[1] + (reverse_slope * (x - c[0]))


def is_projection_between_ab_line(a, b, d):
    total_dist = np.round(calculate_euclidean_distance(a, b), 2)
    return total_dist == (np.round(calculate_euclidean_distance(a, d), 2) +
                          np.round(calculate_euclidean_distance(b, d), 2))


def get_orthogonal_projection(a, b, c):
    projection_point = [None, None]
    if a[0] == b[0]:
        projection_point[0] = a[0]
        projection_point[1] = c[1]
    elif a[1] == b[1]:
        projection_point[0] = c[0]
        projection_point[1] = a[1]
    else:
        slope = calculate_slope(a, b)
        reverse_slope = - 1 / slope
        projection_point[0] = calculate_projection_x(a, c, slope, reverse_slope)
        projection_point[1] = calculate_projection_y(c, reverse_slope, projection_point[0])
    if not is_projection_between_ab_line(a, b, projection_point):
        return False
    return projection_point
