import streamlit as st
import pandas as pd
from src.core.login import enforce_login
from src.core.state import initialise_state
from src.ui.screens.program_builder.nav import render_program_builder_tabs
from src.ui.screens.program_builder.state import init_program_builder_state

st.set_page_config(layout="wide")
enforce_login() # Auth check on every page
initialise_state() # Initialises app-level state to prevent deep-link crashes
init_program_builder_state() # Initialises state at the page level
# Set the entry point screen for the Desktop and Mobile tabs.
if st.session_state.program_builder_desktop_screen is None:
    st.session_state.program_builder_desktop_screen = 'dimensions_form'
if st.session_state.program_builder_mobile_screen is None:
    st.session_state.program_builder_mobile_screen = 'dimensions_form'

st.title("Program Builder")
render_program_builder_tabs() # Renders Tabs for page-level navigation.
# Tabs have conditional rendering logic based on the session state initialised on this page (init_program_builder_state)






