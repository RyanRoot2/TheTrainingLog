import streamlit as st
from src.core.data_transform import flatten_day_to_dataframe
from src.ui.screens.mobile_week_select import render_mobile_week_select
from src.ui.screens.mobile_day_select import render_mobile_day_select
from src.ui.screens.mobile_day_view import render_mobile_day_view


#--- Functions to navigate between screens ---
def render_current_screen():
    if st.session_state.current_screen == 'week_select':
        render_mobile_week_select()

    elif st.session_state.current_screen == 'day_select':
        render_mobile_day_select()
        
    elif st.session_state.current_screen == 'day_view':
        render_mobile_day_view()
