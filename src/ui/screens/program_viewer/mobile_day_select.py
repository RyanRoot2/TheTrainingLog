import streamlit as st
from src.ui.screens.program_viewer.components.select_grid import render_grid

def render_mobile_day_select():
    if st.session_state.program_viewier_mobile_current_screen == 'day_select': # Technically redundant as check is made before function call
        selected_week_num = st.session_state.program_viewer_mobile_selected_week
        program_week = st.session_state.program_json["program"]["weeks"][f"week_{selected_week_num}"]
        render_grid("Day", program_week, 1, 'day_view')