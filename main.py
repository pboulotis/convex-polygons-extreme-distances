import streamlit as st
from algorithm import handle_page
from start import show_polygon_page, visualize_polygons, update_vertices
from init import show_initial_phase_page, get_p_q_lists
from tester import handle_test


def show_home_page():
    st.title("Minimum distance between two convex polygons")
    st.write("Choose one of the following examples or go to the 'Polygon coordinates' page from the sidebar "
             "on the left, in order to start the algorithm.")
    example = st.selectbox("Create your own polygons or pick an existing example:",
                           ["Example 1", "Example 2", "Example 3", "New"])
    if example == "New":
        update_vertices([], "P")
        update_vertices([], "Q")
        return
    elif example == "Example 1":
        vertices1 = [(0, 0), (0.5, 0), (1, 0.5), (0.5, 1), (0, 1), (-0.5, 0.5)]
        vertices2 = [(2, 1.5), (2.5, 2.5), (1.75, 3), (1, 2.5), (1.5, 1.5)]
        update_vertices(vertices1, "P")
        update_vertices(vertices2, "Q")
    st.plotly_chart(visualize_polygons())


def show_algorithm_page():
    st.title("Binary Elimination")

    p_list, q_list = get_p_q_lists()
    if not p_list or not q_list:
        st.warning("Complete the initial phase first by selecting it from the sidebar on the left")
    else:
        st.write("For the following steps we will name the first vertex of P' (u') as p1 and the last (u'') as p2.")
        st.write("Likewise for the Q' the last vertex (w') as q1 and the first (w'') as q2, due to the counter "
                 "clockwise assignment of the vertices.")
        handle_page(p_list, q_list)


def show_final_phase_page():
    st.title("Final Phase")


def show_tester_page():
    handle_test()


if __name__ == "__main__":
    page = st.sidebar.selectbox("Select Page", ["Home", "Polygon coordinates", "Initial Phase",
                                                "Algorithm", "Final Phase", "Tester"])
    if page == "Home":
        show_home_page()
    elif page == "Polygon coordinates":
        show_polygon_page()
    elif page == "Initial Phase":
        show_initial_phase_page()
    elif page == "Algorithm":
        show_algorithm_page()
    elif page == "Tester":
        show_tester_page()
    else:
        show_final_phase_page()
