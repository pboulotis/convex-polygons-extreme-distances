import streamlit as st
import plotly.graph_objs as go

from utils import is_convex_polygon, convert_counterclockwise

vertices1, vertices2 = [], []


class VertexInput:
    def __init__(self, label):
        self.label = label

    def write(self):
        columns = st.columns([1, 1])
        x = columns[0].text_input(f"x{self.label}:")
        y = columns[1].text_input(f"y{self.label}:")
        return float(x) if x else None, float(y) if y else None


def get_polygon_vertices(polygon_name):
    global vertices1, vertices2
    if polygon_name == "P":
        return vertices1
    return vertices2


def update_vertices(new_vertices, polygon_name):
    global vertices1, vertices2
    if new_vertices and not is_convex_polygon(new_vertices):
        st.error(f"The {polygon_name} polygon is not convex, check the vertices again and"
                 f" that you have typed the coordinates counter clockwise")
    if polygon_name == "P":
        vertices1 = new_vertices
    else:
        vertices2 = new_vertices


def show_polygon_page():
    st.title("Initialize Polygons")

    selected_tab = st.radio("Select Polygon", ["Polygon P", "Polygon Q"])

    if selected_tab == "Polygon P":
        initialize_polygon_tab("P")
    else:
        initialize_polygon_tab("Q")
    st.subheader("Plot visualization")
    st.plotly_chart(visualize_polygons(), use_container_width=True)


def handle_input_file(polygon_name):
    txt_file = st.file_uploader(f"Upload .txt file for Polygon {polygon_name}", type=['txt'])
    if txt_file is not None:
        st.info("The .txt file needs to be in the form: x1,y1 x2,y2 x3,y3 e.g. 0,0 1,1 0,1")
        if not txt_file.name.lower().endswith(".txt"):
            st.error(f"Invalid file type. Please upload a .txt file for Polygon {polygon_name}.")
            return
        file_contents = txt_file.read()

        lines = file_contents.decode().splitlines()
        vertices = []
        for line in lines:
            try:
                x, y = map(float, line.split(','))
                vertices.append((x, y))
            except ValueError:
                st.warning(f"Invalid format in line: {line}. Please use the format 'x,y'. Skipping this line.")
        update_vertices(vertices, polygon_name)


def initialize_vertices(num_vertices, vertices, polygon_name):
    if not vertices:
        vertices = []
    st.subheader(f"Type the (x,y) coordinates of the {num_vertices} vertices of the polygon:")

    for i in range(num_vertices):
        x, y = VertexInput(f"{i + 1}").write()
        if x is not None and y is not None:
            vertices.append((x, y))

    update_vertices(vertices, polygon_name)

    return vertices


def add_point(figure, point, color, name):
    figure.add_trace(go.Scatter(x=[point[0]], y=[point[1]], mode='markers',
                                marker=dict(size=12, color=f"{color}"), name=f"{name}"))


def add_line(figure, point, other_point, color, name):
    figure.add_trace(go.Scatter(x=[point[0], other_point[0]], y=[point[1], other_point[1]], mode='lines',
                                line=dict(color=f'{color}'), name=f"{name}"))


def add_vertices(figure, vertices, color, name):
    if len(vertices) > 1:
        x, y = zip(*vertices)
        figure.add_trace(go.Scatter(x=list(x), y=list(y), mode='lines+markers',
                                    marker=dict(size=10), line=dict(color=f'{color}'), name=f"{name}"))


def visualize_polygons():
    global vertices1, vertices2
    figure = go.Figure()
    figure.update_xaxes(
        scaleanchor="y",
        scaleratio=1,
    )
    # figure.update_layout(width=650, height=650)
    if len(vertices1) > 0 and is_convex_polygon(vertices1):
        x1, y1 = zip(*vertices1)
        figure.add_trace(go.Scatter(x=list(x1) + [x1[0]], y=list(y1) + [y1[0]], mode='lines+markers',
                                    marker=dict(size=10), line=dict(color='blue'), name="Polygon P"))
    else:
        add_vertices(figure, vertices1, "blue", "Polygon P")

    if len(vertices2) > 0 and is_convex_polygon(vertices2):
        x2, y2 = zip(*vertices2)
        figure.add_trace(go.Scatter(x=list(x2) + [x2[0]], y=list(y2) + [y2[0]], mode='lines+markers',
                                    marker=dict(size=10), line=dict(color='orange'), name="Polygon Q"))
    else:
        add_vertices(figure, vertices2, "orange", "polygon Q")

    return figure


def initialize_polygon_tab(polygon_name):
    handle_input_file(polygon_name)
    vertices = get_polygon_vertices(polygon_name)
    selected_option = st.checkbox(f"Type the coordinates manually for {polygon_name}")
    if selected_option:
        update_vertices([], polygon_name)
        num_vertices = st.number_input(f"How many vertices do you want to enter for {polygon_name}?",
                                       min_value=3, max_value=20, value=3, step=1)
        vertices = initialize_vertices(num_vertices, vertices, polygon_name)
        reset = st.button(f"Reset {polygon_name} coordinates")
        if reset:
            update_vertices([], polygon_name)
            # st.session_state.selected_option = not st.session_state.checkbox_state

    st.write("If these are the coordinates you want, press the following button:")
    locked = st.button(f"Lock coordinates for {polygon_name}")
    if locked:
        vertices = convert_counterclockwise(vertices)
        update_vertices(vertices, polygon_name)
