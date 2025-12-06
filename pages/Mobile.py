import streamlit as st
from src.utils.streamlit_temp_auth import check_st_authentication
from src.core.state import set_current_screen
from src.backend.firestore import program
from src.ui.navigation import render_current_screen


check_st_authentication()
set_current_screen()
render_current_screen()
