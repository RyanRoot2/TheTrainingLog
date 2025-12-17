import streamlit as st
import pandas as pd
from src.core.login import enforce_login
from src.core.state import initialise_state
from src.ui.components.program_builder_dimensions import get_program_dimensions
from src.ui.screens.program_builder.nav import render_program_builder_tabs
from src.ui.screens.program_builder.state import init_program_builder_state

enforce_login() # Auth check on every page
initialise_state() # Initialises app-level state to prevent deep-link crashes

init_program_builder_state() # Initialises state at the page level
st.set_page_config(layout="wide")


st.title("Program Builder")
render_program_builder_tabs() # Renders Tabs for page-level navigation.
# Tabs have conditional rendering logic based on the session state initialised on this page (init_program_builder_state)






