# src/core/state.py
import streamlit as st

def initialise_state():
    """Initializes session state variables for UI navigation and selection."""

    if 'user_uid' not in st.session_state:
        st.session_state.user_uid = None
    
    if 'is_logged_in' not in st.session_state:
        st.session_state.is_logged_in = None

    if 'user_email' not in st.session_state:
        st.session_state.user_email = None



        



def nav_to(screen):
    st.session_state.current_screen = screen
    st.rerun()


def reset_to_home():
    st.session_state.selected_week = None
    st.session_state.selected_day = None
    nav_to('week_select')
    st.rerun()


def set_current_screen():
    week_selected = st.session_state.get('selected_week')
    day_selected = st.session_state.get('selected_day')

    if day_selected is not None:
        st.session_state.current_screen = 'day_view'

    elif week_selected is not None:
        st.session_state.current_screen = 'day_select'

    else:
        st.session_state.current_screen = 'week_select'