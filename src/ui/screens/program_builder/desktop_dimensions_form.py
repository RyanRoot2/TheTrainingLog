import streamlit as st

def render_desktop_dimensions_form():
    with st.form("program_structure_form", clear_on_submit=False):
        col1, col2 = st.columns(2)

        with col1:
            num_weeks = st.number_input('Number of Weeks', min_value=1, max_value=12, value=1, key="num_weeks")
        with col2:
            num_days = st.number_input('Number of Days', min_value=1, max_value=7, value=4, key='num_days')

        submitted = st.form_submit_button("Go to next step")

        if submitted:
            st.session_state.program_builder_desktop_num_weeks = num_weeks
            st.session_state.program_builder_desktop_num_days = num_days
            st.session_state.desktop_program_builder_screen = 'movement_selection'
            st.rerun() # Change to a callback