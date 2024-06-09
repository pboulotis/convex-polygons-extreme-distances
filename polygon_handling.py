import streamlit as st
import plotly.graph_objs as go

from utils import is_convex_polygon, convert_counterclockwise, check_polygon_intersection

polygon_p, polygon_q = [], []


class VertexInput:
    def __init__(self, label):
        self.label = label

    def write(self):
        columns = st.columns([1, 1])
        x = columns[0].text_input(f"x{self.label}:")
        y = columns[1].text_input(f"y{self.label}:")
        return float(x) if x else None, float(y) if y else None


def get_polygon_vertices(polygon_name):
    global polygon_p, polygon_q
    if polygon_name == "P":
        return polygon_p
    return polygon_q


def update_vertices(new_vertices, polygon_name):
    global polygon_p, polygon_q
    if new_vertices and not is_convex_polygon(new_vertices):
        st.error(f"The {polygon_name} polygon is not convex, check the vertices again and"
                 f" that you have typed the coordinates in the correct order")
    if polygon_name == "P":
        polygon_p = convert_counterclockwise(new_vertices)
    else:
        polygon_q = convert_counterclockwise(new_vertices)


def intersection_exists():
    possible_intersection = check_polygon_intersection(polygon_p, polygon_q)
    if possible_intersection:
        st.warning("We cannot execute the algorithm for minimum distance since the polygons intersect")
        return possible_intersection
    return None


def handle_input_file(vertices, polygon_name):
    txt_file = st.file_uploader(f"Upload .txt file for Polygon {polygon_name}", type=['txt'])
    if txt_file is None:
        return
    st.info("The .txt file needs to be in the form: x1,y1 x2,y2 x3,y3 e.g. 0,0 1,1 0,1. "
            "Unselect it if you want to type the coordinates manually")
    if not txt_file.name.lower().endswith(".txt"):
        st.error(f"Invalid file type. Please upload a .txt file for Polygon {polygon_name}.")
        return
    file_contents = txt_file.read()
    file_lines = file_contents.decode().splitlines()
    for line in file_lines:
        try:
            x, y = map(float, line.split(','))
            vertices.append((x, y))
        except ValueError:
            st.warning(f"Invalid format in line: {line}. Please use the format 'x,y'. Skipping this line...")
    if vertices:
        vertices = convert_counterclockwise(vertices)
        update_vertices(vertices, polygon_name)


def initialise_vertices_manually(num_vertices, vertices, polygon_name):
    if not vertices:
        vertices = []
    st.subheader(f"Type the (x,y) coordinates of the {num_vertices} vertices of the polygon {polygon_name}:")

    for i in range(num_vertices):
        x, y = VertexInput(f"{i + 1}").write()
        if x is not None and y is not None:
            vertices.append((x, y))

    # update_vertices(vertices, polygon_name)

    return vertices


def initialise_polygon_coordinates_tab(polygon_name):
    vertices = get_polygon_vertices(polygon_name)
    handle_input_file(vertices, polygon_name)

    selected_option = st.checkbox(f"Type the coordinates manually for {polygon_name}")
    if selected_option:
        vertices = []
        num_vertices = st.number_input(f"How many vertices do you want to enter for {polygon_name}?",
                                       min_value=3, max_value=100, value=3, step=1)
        vertices = initialise_vertices_manually(num_vertices, vertices, polygon_name)

        reset = st.button(f"Reset {polygon_name} coordinates")
        if reset:
            vertices = []
            update_vertices([], polygon_name)

        if len(vertices) > 0 and is_convex_polygon(vertices):
            st.write("The polygon (so far):")
            figure = go.Figure()
            figure.update_xaxes(scaleanchor="y", scaleratio=1)
            draw_polygon(figure, vertices, "grey", f"{polygon_name}")
            st.plotly_chart(figure)

    st.write("If these are the coordinates you want, press the following button:")
    locked = st.button(f"Lock coordinates for {polygon_name}")
    if locked:
        vertices = convert_counterclockwise(vertices)
        update_vertices(vertices, polygon_name)


def draw_point(figure, point, color, name):
    figure.add_trace(go.Scatter(x=[point[0]], y=[point[1]], mode='markers',
                                marker=dict(size=12, color=f"{color}"), name=f"{name}"))


def draw_line(figure, point, other_point, color, name):
    figure.add_trace(go.Scatter(x=[point[0], other_point[0]], y=[point[1], other_point[1]], mode='lines',
                                line=dict(color=f'{color}'), name=f"{name}"))


def draw_vertices(figure, vertices, color, name):
    if len(vertices) > 1:
        x, y = zip(*vertices)
        figure.add_trace(go.Scatter(x=list(x), y=list(y), mode='lines+markers',
                                    marker=dict(size=10), line=dict(color=f'{color}'), name=f"{name}"))


def draw_polygon(figure, polygon, color, name):
    x, y = zip(*polygon)
    figure.add_trace(go.Scatter(x=list(x) + [x[0]], y=list(y) + [y[0]], mode='lines+markers',
                                marker=dict(size=10), line=dict(color=f'{color}'), name=f"Polygon {name}"))


def visualise_polygons():
    global polygon_p, polygon_q
    figure = go.Figure()
    figure.update_xaxes(scaleanchor="y", scaleratio=1)
    # figure.update_layout(width=650, height=650)

    if len(polygon_p) > 0 and is_convex_polygon(polygon_p):
        draw_polygon(figure, polygon_p, "cyan", "P")
    else:
        draw_vertices(figure, polygon_p, "cyan", "Polygon P")

    if len(polygon_q) > 0 and is_convex_polygon(polygon_q):
        draw_polygon(figure, polygon_q, "orange", "Q")
    else:
        draw_vertices(figure, polygon_q, "orange", "Polygon Q")

    return figure
