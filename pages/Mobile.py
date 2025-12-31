import streamlit as st
from src.core.login import enforce_login
from src.core.state import initialise_state
from src.ui.screens.program_viewer.state import init_program_viewer_state
from src.ui.screens.program_viewer.nav import render_current_screen
from src.backend.firestore import load_active_program_json

st.set_page_config(layout="wide")
enforce_login() # Auth check on every page
initialise_state() # Initialises app-level state to prevent deep-link crashes
init_program_viewer_state() # Initialises state at the page level

# Set Initial Screen to 'week_select' as entry point
if st.session_state.program_viewier_mobile_current_screen is None:
    st.session_state.program_viewier_mobile_current_screen = 'week_select'

# Load Program Data JSON
# Initialize program stats in session state if not already set
# Required for render functions
program_json = load_active_program_json()
if 'active_program_weeks' not in st.session_state or st.session_state.active_program_weeks is None:
    st.session_state.active_program_weeks = program_json["stats"]["weeks"]
if 'active_program_days_per_week' not in st.session_state or st.session_state.active_program_days_per_week is None:
    st.session_state.active_program_days_per_week = program_json["stats"]["days_per_week"]
if st.session_state.program_json is None:
    st.session_state.program_json = program_json
# Will investigate loading the program elsewhere with a cache, and then setting weeks and days in the init function

st.write(program_json)

# Render the current screen based on session state - chosen weeks and days
render_current_screen()