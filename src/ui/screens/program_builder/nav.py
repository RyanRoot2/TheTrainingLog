import streamlit as st
from src.ui.screens.program_builder.desktop_dimensions_form import render_desktop_dimensions_form
from src.ui.screens.program_builder.desktop_movement_selection import render_desktop_movement_selection
from src.ui.screens.program_builder.desktop_progressions import render_desktop_progressions
from src.ui.screens.program_builder.state import (
    init_desktop_dimensions_form_state,
    init_desktop_movement_selection_state,
    init_desktop_progressions_state
)


def render_program_builder_tabs():
    mobile, desktop, settings = st.tabs([
        "Mobile",
        "Desktop",
        "Settings"
    ])
    with mobile:
        st.info("👋 Mobile version under construction! Check out the desktop page!")
    with desktop:
        if st.session_state.program_builder_desktop_screen == 'dimensions_form':
            init_desktop_dimensions_form_state()
            render_desktop_dimensions_form()
        elif st.session_state.program_builder_desktop_screen == 'movement_selection':
            num_days = st.session_state.program_builder_desktop_num_days
            init_desktop_movement_selection_state(num_days)
            render_desktop_movement_selection(num_days)
        elif st.session_state.program_builder_desktop_screen == 'progressions':
            init_desktop_progressions_state()
            render_desktop_progressions()
    with settings:
        st.info("👋 Let me know what kind of functionality you'd like to see! Day x Week versus Week x Day layout? Saved progressons for quicker building?")


