import streamlit as st
from src.ui.components.grid import render_grid
from src.backend.firestore import program

def render_mobile_week_select():
    if st.session_state.current_screen == 'week_select': # Technically redundant as check is made before function call
            render_grid("Week", program["weeks"], number_of_columns=1, screen_to_nav_to='day_select')