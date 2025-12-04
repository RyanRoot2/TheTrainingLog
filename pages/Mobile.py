import streamlit as st
from src.utils.streamlit_temp_auth import check_st_authentication
from src.backend.firestore import program
from src.ui.navigation import render_grid, render_movements_and_sets


check_st_authentication()

if 'current_screen' not in st.session_state:
    st.session_state.current_screen = 'week_select'

if 'selected_week' in st.session_state and 'selected_day' not in st.session_state:
    st.session_state.current_screen = 'day_select'

if 'selected_week' and 'selected_day' in st.session_state:
    st.session_state.current_screen = 'day_view'


if st.session_state.current_screen == 'week_select':
    render_grid("Week", program["weeks"], 3, 'day_select') 
elif st.session_state.current_screen == 'day_select':
    selected_week_num = st.session_state.selected_week
    program_week = program["weeks"][f"week_{selected_week_num}"]
    render_grid("Day", program_week, 1, 'day_view')
elif st.session_state.current_screen == 'day_view':
    selected_week_num = st.session_state.selected_week
    selected_day_num = st.session_state.selected_day
    st.subheader(f"Workout for Week {selected_week_num}, Day {selected_day_num}")
    day_data = program["weeks"][f"week_{selected_week_num}"][f"day_{selected_day_num}"]
    render_movements_and_sets(day_data, key_label=f"week_{selected_week_num}_day_{selected_day_num}_editor")

st.write(st.session_state)
