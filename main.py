import streamlit as st
from algorithm import handle_algorithm_page, binary_elimination_no_display
from final import show_min_distance_result
from max_dist import show_max_dist_page
from polygon_handling import visualise_polygons, update_vertices, initialize_polygon_coords_tab, get_polygon_vertices
from init import show_initial_phase_page, get_p_q_lists, set_p_q_lists, get_initial_phase_result_no_display
from tester import handle_test
from utils import check_polygon_intersection


def execute_only_algorithm():
    p_list, q_list = get_initial_phase_result_no_display()
    p_list, q_list = binary_elimination_no_display(p_list, q_list)
    set_p_q_lists(p_list, q_list)
    show_min_distance_result()


def handle_min_buttons():
    polygon_p, polygon_q = get_polygon_vertices("P"), get_polygon_vertices("Q")
    if not polygon_p or not polygon_q:
        return
    column1, column2 = st.columns(2)
    with column1:
        button1 = st.empty()
    with column2:
        button2 = st.empty()
    visual_button = button1.button("Min distance visualization")
    result_button = button2.button("Min distance result only")
    if visual_button:
        button1.empty()
        button2.empty()
        show_initial_phase_page()
        show_algorithm_page()
        show_final_phase_page()

    if result_button:
        button2.empty()
        execute_only_algorithm()
        st.write("You can see all the visualization stages by selecting the pages from the sidebar on the left")


def handle_max_buttons():
    polygon_p, polygon_q = get_polygon_vertices("P"), get_polygon_vertices("Q")
    if not polygon_p or not polygon_q:
        return
    st.write("----------------------------------------------------------")
    column1, column2 = st.columns(2)
    with column1:
        button3 = st.empty()
    with column2:
        button4 = st.empty()
    visual_button = button3.button("Max distance visualization")
    result_button = button4.button("Max distance result only")
    if visual_button:
        button3.empty()
        button4.empty()
        show_max_dist_page()

    if result_button:
        button4.empty()
        show_max_dist_page(display=False)


def show_home_page():
    st.title("Extreme distances between two convex polygons")
    example = st.selectbox("Create your own polygons with 'New' or pick an existing example:",
                           ["Example 1", "Example 2", "Example 3", "New"])
    polygon_p, polygon_q = [], []
    if example == "New":
        update_vertices([], "P")
        update_vertices([], "Q")
        show_polygon_page()
        return
    elif example == "Example 1":
        polygon_p = [(0, 0), (0.5, 0), (1, 0.5), (0.5, 1), (0, 1), (-0.5, 0.5)]
        polygon_q = [(2.25, 1.5), (2.5, 2.5), (1.75, 3), (1, 2.5), (1.25, 1.5)]
    update_vertices(polygon_p, "P")
    update_vertices(polygon_q, "Q")
    st.plotly_chart(visualise_polygons())

    possible_intersection = check_polygon_intersection(polygon_p, polygon_q)
    if possible_intersection:
        st.write(f"The two polygons intersect on the points: {possible_intersection}")

    handle_min_buttons()
    handle_max_buttons()


def show_polygon_page():
    st.subheader("Initialize Polygons")

    selected_tab = st.radio("Select Polygon", ["Polygon P", "Polygon Q"])

    if selected_tab == "Polygon P":
        initialize_polygon_coords_tab("P")
    else:
        initialize_polygon_coords_tab("Q")
    st.write("Plot visualization")
    st.plotly_chart(visualise_polygons(), use_container_width=True)

    handle_min_buttons()
    handle_max_buttons()


def show_algorithm_page():
    st.subheader("Binary Elimination")

    p_list, q_list = get_p_q_lists()
    if not p_list or not q_list:
        st.warning("Go to the 'Initial Phase' tab first by selecting it from the sidebar on the left")
    else:
        st.write("For the following steps we will name the first vertex of P' (u') as p₁ and the last (u'') as p₂.")
        st.write("Likewise for the Q' the last vertex (w') as q₁ and the first (w'') as q₂, due to the counter "
                 "clockwise assignment of the vertices.")
        p_list, q_list = handle_algorithm_page(p_list, q_list)
        set_p_q_lists(p_list, q_list)


def show_final_phase_page():
    st.subheader("Final Phase")

    p_list, q_list = get_p_q_lists()
    if not p_list or not q_list:
        st.warning("Go to the 'Algorithm' tab first by selecting it from the sidebar on the left")
    else:
        show_min_distance_result(show_all_possibilities=True)


def show_tester_page():
    handle_test()


if __name__ == "__main__":
    page = st.sidebar.selectbox("Select Page", ["Home", "Initial Phase",
                                                "Algorithm", "Final Phase", "Tester", "Maximum Distance"])
    if page == "Home":
        show_home_page()
    elif page == "Initial Phase":
        show_initial_phase_page()
    elif page == "Algorithm":
        show_algorithm_page()
    elif page == "Tester":
        show_tester_page()
    elif page == "Final Phase":
        show_final_phase_page()
    else:
        show_max_dist_page()
