import streamlit as st
import plotly.graph_objs as go

from geometry_utils import is_polygon_position_correct, is_convex_polygon
from polygon_handling import visualise_polygons, update_vertices, initialise_polygon_coordinates_tab, \
    get_polygon_vertices, intersection_exists, draw_point, internal_polygon_exists
from algorithm_init import show_initial_phase_page, get_p_q_lists, set_p_q_lists, get_initial_phase_result_no_display
from algorithm import handle_algorithm_page, binary_elimination_no_display
from algorithm_final import show_min_distance_result
from max_distance import show_max_distance_page


def execute_only_algorithm(polygon_p, polygon_q):
    p_list, q_list = get_initial_phase_result_no_display(polygon_p, polygon_q)
    p_list, q_list = binary_elimination_no_display(p_list, q_list)
    set_p_q_lists(p_list, q_list)
    show_min_distance_result()


def handle_buttons(polygon_p, polygon_q, label):
    if not polygon_p or not polygon_q:
        return
    column1, column2 = st.columns(2)
    with column1:
        button1 = st.empty()
    with column2:
        button2 = st.empty()
    visual_button = button1.button(f"{label} distance visualization")
    result_button = button2.button(f"{label} distance result only")
    if visual_button:
        button1.empty()
        button2.empty()
        if label == "Minimum":
            show_initial_phase_page()
            show_algorithm_page()
            show_final_phase_page()
        else:
            show_max_distance_page(display=True)
    if result_button:
        button2.empty()
        if label == "Minimum":
            execute_only_algorithm(polygon_p, polygon_q)
            st.write("You can see all the visualization stages by selecting the pages from the sidebar on the left")
        else:
            show_max_distance_page()


def handle_intersection_and_buttons(polygon_p, polygon_q):
    possible_intersection = intersection_exists()
    if possible_intersection:
        figure = visualise_polygons()
        if isinstance(possible_intersection, tuple):
            st.write(f"The two polygons intersect on the point: {possible_intersection}")
            st.write("Therefore the minimum distance is 0, achieved by the intersection point as shown below:")
            draw_point(figure, possible_intersection, "red", "Intersection point")
        else:
            st.write(f"The two polygons intersect on the points: {possible_intersection}")
            st.write("Therefore the minimum distance is 0, achieved by the intersection points as shown below:")
            points = go.Scatter(
                x=[point[0] for point in possible_intersection],
                y=[point[1] for point in possible_intersection],
                mode='markers', name='Intersection points', marker=dict(color='red', size=10)
            )
            figure.add_trace(points)
        st.plotly_chart(figure)
        handle_buttons(polygon_p, polygon_q, "Maximum")
        return
    if not internal_polygon_exists():
        handle_buttons(polygon_p, polygon_q, "Minimum")
    st.write("---")
    handle_buttons(polygon_p, polygon_q, "Maximum")


def enter_polygon_coordinates():
    st.subheader("Initialize Polygons")
    selected_tab = st.radio("Select Polygon, Polygon P (left) and Polygon Q (right)", ["Polygon P", "Polygon Q"])

    if selected_tab == "Polygon P":
        initialise_polygon_coordinates_tab("P")
    elif selected_tab == "Polygon Q":
        initialise_polygon_coordinates_tab("Q")

    polygon_p, polygon_q = get_polygon_vertices("P"), get_polygon_vertices("Q")

    if polygon_p and polygon_q and not is_polygon_position_correct(polygon_p, polygon_q):
        # Swap the polygon coordinates
        st.info("The polygons where given incorrect positions, switching the coordinates")
        temp = polygon_p
        update_vertices(polygon_q, "P")
        update_vertices(temp, "Q")
        polygon_p = polygon_q
        polygon_q = temp
    st.subheader("Visualization of both polygons")
    st.plotly_chart(visualise_polygons(), use_container_width=True)

    if len(polygon_p) < 3 or len(polygon_q) < 3:
        return

    handle_intersection_and_buttons(polygon_p, polygon_q)


def show_algorithm_page():
    st.subheader("Binary Elimination")
    if intersection_exists() or internal_polygon_exists():
        return

    p_list, q_list = get_p_q_lists()
    if not p_list or not q_list:
        st.warning("Go to the 'Initial Phase' tab first by selecting it from the sidebar on the left")
    else:
        st.write("For the following steps we will name the first vertex of P' (u') as p₁ and the last (u'') as p₂.")
        st.write("Likewise for the Q' the last vertex (w') as q₁ and the first (w'') as q₂, due to the counter "
                 "clockwise assignment of the vertices.")
        p_list, q_list = handle_algorithm_page(p_list, q_list)
        set_p_q_lists(p_list, q_list)


def show_final_phase_page(sidebar=False):
    st.subheader("Final Phase")
    if intersection_exists() or internal_polygon_exists():
        return
    if sidebar:
        st.warning("If you have not, go to the 'Binary Elimination' tab first to get the proper results")
    p_list, q_list = get_p_q_lists()
    if not p_list or not q_list:
        st.warning("Go to the 'Binary Elimination' tab first by selecting it from the sidebar on the left")
    else:
        show_min_distance_result(show_all_possibilities=True)


def show_home_page():
    st.title("Extreme distances between two convex polygons")
    options = ["Select", "Example 1", "Example 2", "Example 3", "Example 4", "Example 5", "Example 6", "New"]
    example = st.selectbox("Create your own polygons with 'New' or pick an existing example:", options)
    polygon_p, polygon_q = get_polygon_vertices("P"), get_polygon_vertices("Q")
    if example == "Select":
        if not polygon_p and not polygon_q:
            return
    elif example == "New":
        if polygon_p or polygon_q:
            st.write("If you don't want these polygons:")
            reset = st.button("Reset the coordinates")
            if reset:
                update_vertices([], "P")
                update_vertices([], "Q")
        enter_polygon_coordinates()
        return
    elif example == "Example 1":
        polygon_p = [(0, 0), (0.5, 0), (1, 0.5), (0.5, 1), (0, 1), (-0.5, 0.5)]
        polygon_q = [(2.25, 1.5), (2.5, 2.5), (1.75, 3), (1, 2.5), (1.25, 1.5)]
    elif example == "Example 2":
        polygon_p = [(1, 1), (5, 1), (7, 3), (5, 5), (1, 5)]
        polygon_q = [(6, 3), (7, 1), (10, 1), (10, 5), (7, 5)]
    elif example == "Example 3":
        polygon_p = [(1, 1), (5, 1), (6, 3), (5, 5), (1, 5)]
        polygon_q = [(6, 3), (7, 1), (10, 1), (10, 5), (7, 5)]
    elif example == "Example 4":
        polygon_p = [(1, 1), (5, 1), (6, 2), (6, 4), (5, 5), (1, 5)]
        polygon_q = [(6, 2), (7, 1), (10, 1), (10, 5), (7, 5), (6, 4)]
    elif example == "Example 5":
        polygon_p = [(0, 0), (2, 0), (3, 1), (3, 2), (2, 3), (0, 3), (-1, 2), (-1, 1)]
        polygon_q = [(0.5, 1), (1.5, 1), (1.75, 1.5), (1.5, 2), (0.5, 2)]
    elif example == "Example 6":
        polygon_p = [(2, 0), (4, 0), (6, 2), (4, 4), (2, 4), (0, 2)]
        polygon_q = [(11, 2), (13, 2), (14, 4), (12, 6), (10, 4)]

    update_vertices(polygon_p, "P")
    update_vertices(polygon_q, "Q")
    st.plotly_chart(visualise_polygons())

    if is_convex_polygon(polygon_p) and is_convex_polygon(polygon_q):
        handle_intersection_and_buttons(polygon_p, polygon_q)


if __name__ == "__main__":
    page = st.sidebar.selectbox("Select Page", ["Home", "Initial Phase",
                                                "Binary Elimination", "Final Phase", "Maximum Distance"])
    if page == "Home":
        show_home_page()
    elif page == "Initial Phase":
        show_initial_phase_page(sidebar=True)
    elif page == "Binary Elimination":
        show_algorithm_page()
    elif page == "Final Phase":
        show_final_phase_page(sidebar=True)
    else:
        show_max_distance_page(display=True)
