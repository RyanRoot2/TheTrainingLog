import streamlit as st
from src.ui.screens.program_viewer.components.select_grid import render_grid

def render_mobile_week_select():
    if st.session_state.program_viewier_mobile_current_screen == 'week_select': # Technically redundant as check is made before function call
            render_grid("Week", st.session_state.program_json["program"]["weeks"], number_of_columns=1, screen_to_nav_to='day_select')