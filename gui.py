import streamlit as st
from start import show_polygon_page, visualize_polygons, update_vertices
from tester2 import show_initial_phase_page


def show_home_page():
    st.title("Minimum distance between two convex polygons")
    st.write("Choose one of the following examples or go to the 'Polygon coordinates' page from the sidebar,"
             " in order to start the algorithm.")
    example = st.selectbox("Create your own polygons or pick an existing example:",
                           ["Example 1", "Example 2", "Example 3", "New"])
    if example == "New":
        return
    elif example == "Example 1":
        vertices1 = [(0, 0), (0.5, 0), (1, 0.5), (0.5, 1), (0, 1), (-0.5, 0.5)]
        vertices2 = [(2, 1.5), (2.5, 2.5), (1.75, 3), (1, 2.5), (1.5, 1.5)]
        update_vertices(vertices1, "P")
        update_vertices(vertices2, "Q")
    st.plotly_chart(visualize_polygons())


def show_algorithm_page():
    st.title("Binary Elimination")


if __name__ == "__main__":
    page = st.sidebar.selectbox("Select Page", ["Home", "Polygon coordinates", "Initial Phase", "Algorithm"])
    if page == "Home":
        show_home_page()
    elif page == "Polygon coordinates":
        show_polygon_page()
    elif page == "Initial Phase":
        show_initial_phase_page()
    else:
        show_algorithm_page()
