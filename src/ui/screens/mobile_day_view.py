import streamlit as st
from src.ui.components.workout_data_editor import render_movements_and_sets
from src.ui.components.mobile_day_view_tabs import render_mobile_day_view_week_navigation, render_mobile_day_view_day_navigation
from src.backend.firestore import program

def render_mobile_day_view():
    if st.session_state.current_screen == 'day_view': # Technically redundant as check is made before function call
            selected_week_num = st.session_state.selected_week
            selected_day_num = st.session_state.selected_day
            with st.expander("Quick Navigation"):
                render_mobile_day_view_week_navigation()
                render_mobile_day_view_day_navigation()
            st.subheader(f"Workout for Week {selected_week_num}, Day {selected_day_num}")
            day_data = program["weeks"][f"week_{selected_week_num}"][f"day_{selected_day_num}"]
            render_movements_and_sets(day_data, key_label=f"week_{selected_week_num}_day_{selected_day_num}_editor")