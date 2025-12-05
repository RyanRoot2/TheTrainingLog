import streamlit as st
from src.utils.streamlit_temp_auth import check_st_authentication
from src.backend.firestore import program
from src.ui.navigation import render_grid, render_movements_and_sets


check_st_authentication()

week_selected = st.session_state.get('selected_week')
day_selected = st.session_state.get('selected_day')

if day_selected is not None:
    st.session_state.current_screen = 'day_view'

elif week_selected is not None:
    st.session_state.current_screen = 'day_select'

else:
    st.session_state.current_screen = 'week_select'



st.write(st.session_state.current_screen)



if st.session_state.current_screen == 'week_select':
    render_grid("Week", program["weeks"], number_of_columns=1, screen_to_nav_to='day_select')

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
