import streamlit as st

def init_program_viewer_state():
    if 'program_viewier_mobile_current_screen' not in st.session_state:
        st.session_state.program_viewier_mobile_current_screen = None
        # Possible values:
        # 'week_select' - User is selecting a week
        # 'day_select'  - User is selecting a day within the week
        # 'day_view'    - User is viewing the day's workout details
        
    # Stores the selected week number (e.g., 1, 5, 12)
    if 'program_viewer_mobile_selected_week' not in st.session_state:
        st.session_state.program_viewer_mobile_selected_week = None

    # Stores the selected day number (e.g., 1, 3, 5)
    if 'program_viewer_mobile_selected_day' not in st.session_state:
        st.session_state.program_viewer_mobile_selected_day = None

    # Program JSON data
    if 'program_json' not in st.session_state:
        st.session_state.program_json = None

    # Active Program ID
    if 'active_program_id' not in st.session_state:
        st.session_state.active_program_id = None




def nav_to(screen_name: str):
    st.session_state.program_viewier_mobile_current_screen = screen_name
    st.rerun()


def clear_program_viewer_state():
    """
    Resets all keys related to the program viewer
    """
    # 1. Identify all keys to remove
    # We look for the main viewer keys and your progression data keys
    keys_to_delete = [
        key for key in st.session_state 
        if key.startswith('program_viewer_')
    ]

    # 2. Delete them from session state
    for key in keys_to_delete:
        del st.session_state[key]