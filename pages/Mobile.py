import streamlit as st
from src.utils.streamlit_temp_auth import check_st_authentication
from src.backend.firestore import program
from src.ui.navigation import render_week_grid_mobile, render_day_grid_mobile


check_st_authentication()
render_week_grid_mobile(program)
render_day_grid_mobile(program['weeks'][f"week_{st.session_state.selected_week}"])


st.write(st.session_state)
