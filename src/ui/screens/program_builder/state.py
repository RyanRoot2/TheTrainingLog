import streamlit as st
import numpy as np
import pandas as pd

def init_program_builder_state():
    """
    Called at the top of the program_builder page.
    """
    # Initialises the "current screen" state for the desktop and mobile tabs
    if 'program_builder_desktop_screen' not in st.session_state:
        st.session_state.program_builder_desktop_screen = None
    if 'program_builder_mobile_screen' not in st.session_state:
        st.session_state.program_builder_mobile_screen = None

def clear_program_builder_state():
    """
    Resets all keys related to the program builder
    """
    # 1. Identify all keys to remove
    # We look for the main builder keys and your progression data keys
    keys_to_delete = [
        key for key in st.session_state 
        if key.startswith('program_builder_')
    ]

    # 2. Delete them from session state
    for key in keys_to_delete:
        del st.session_state[key]

def init_desktop_dimensions_form_state():
    """
    Called when the user starts the desktop program builder
    """
    # Initialises the program builder dimensions
    if 'program_builder_desktop_num_weeks' not in st.session_state:
        st.session_state['program_builder_desktop_num_weeks'] = None
    if 'program_builder_desktop_num_days' not in st.session_state:
        st.session_state['program_builder_desktop_num_weeks'] = None

def init_desktop_movement_selection_state(num_days):
    """
    Called when the user moves to the movement selection page of the desktop program builder
    Uses the dimensions from the previous step to set up a number of data editors
    Sets up session state keys following the feature_streamlit-component pattern
    program_builder_desktop_movement_selection_data_editor_
    """
    column_titles = ['Movement', 'Options']
    starting_rows = 8
    data = []

    for _ in range(starting_rows):
        data.append({'Movement': '', 'Options': []}) # Initialize with explicit empty list

    base_df = pd.DataFrame(data, columns=column_titles)
    
    # Explicitly ensure dtypes for robustness, though numpy with '' should handle it
    base_df = base_df.astype({'Movement': 'object', 'Options': 'object'})

    for i in range(num_days):
        if f'program_builder_desktop_movement_selection_data_{i}' not in st.session_state:
            st.session_state[f'program_builder_desktop_movement_selection_data_{i}'] = base_df.copy()

    # This will hold the program data between screens (Movements, sets, reps, etc)
    if 'program_builder_data' not in st.session_state:
        st.session_state.program_builder_data = None

def init_desktop_progressions_state():
    pass