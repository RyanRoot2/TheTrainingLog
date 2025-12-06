import streamlit as st
from src.ui.components.grid import render_grid
from src.backend.firestore import program

def render_mobile_day_select():
    if st.session_state.current_screen == 'day_select': # Technically redundant as check is made before function call
            selected_week_num = st.session_state.selected_week
            program_week = program["weeks"][f"week_{selected_week_num}"]
            render_grid("Day", program_week, 1, 'day_view')