import streamlit as st
from src.ui.screens.program_builder.desktop_dimensions_form import render_desktop_dimensions_form
from src.ui.screens.program_builder.desktop_movement_selection import render_desktop_movement_selection
from src.ui.screens.program_builder.desktop_progressions import render_desktop_progressions


def render_program_builder_tabs():
    mobile, desktop, settings = st.tabs([
        "Mobile",
        "Desktop",
        "Settings"
    ])
    with mobile:
        st.subheader('Mobile')
    with desktop:
        if st.session_state.desktop_program_builder_screen == 'dimensions_form':
            render_desktop_dimensions_form()
        elif st.session_state.desktop_program_builder_screen == 'movement_selection':
            render_desktop_movement_selection()
        elif st.session_state.desktop_program_builder_screen == 'progressions':
            render_desktop_progressions()
    with settings:
        st.subheader('Settings')


