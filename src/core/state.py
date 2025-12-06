# src/core/state.py
import streamlit as st

def initialise_state():
    """Initializes session state variables for UI navigation and selection."""
    
    # --- UI NAVIGATION STATE ---
    # Tracks the user's current view (e.g., 'week_select', 'workout_view')
    if 'current_screen' not in st.session_state:
        st.session_state.current_screen = None
        # Possible values:
        # 'week_select' - User is selecting a week
        # 'day_select'  - User is selecting a day within the week
        # 'day_view'    - User is viewing the day's workout details
        
    # Stores the selected week number (e.g., 1, 5, 12)
    if 'selected_week' not in st.session_state:
        st.session_state.selected_week = None
        
    # Stores the selected day number (e.g., 1, 3, 5)
    if 'selected_day' not in st.session_state:
        st.session_state.selected_day = None
        
    # --- DATA STATE (for later) ---
    # Tracks the master dataframe for editing
    if 'master_df' not in st.session_state:
        st.session_state.master_df = None
        
    # Tracks the authentication status
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False


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