import streamlit as st
from src.ui.components.program_builder_dimensions import get_program_dimensions
from src.utils.desktop_builder_state_init import initialise_desktop_builder_state
from src.utils.append_desktop_builder_step1_edited_dfs import append_desktop_builder_step1_edited_dfs

# from src.ui.components.desktop_program_builder_column import render_day_column
from src.ui.components.prototype_builder import render_day_column

def render_desktop_program_builder():
    # Ensure we have the number of weeks and days for the program
    if 'builder_num_weeks' not in st.session_state:
        get_program_dimensions()
        st.stop()
   
    num_days = st.session_state.builder_num_days

    # Initialise necessary state variables using dimensions
    initialise_desktop_builder_state(num_days)
    # st.write(st.session_state)

    # Create column structure for each day
    days = st.columns(num_days)

    # Render each column
    for i, col in enumerate(days):
        with col:
            render_day_column(i)

    if st.button("Step 2"):
        program_builder_data_step1 = append_desktop_builder_step1_edited_dfs()
        if program_builder_data_step1 not in st.session_state:
            st.session_state.program_builder_data_step1 = program_builder_data_step1
        st.session_state.desktop_builder_step2 = True
        st.rerun()
        


