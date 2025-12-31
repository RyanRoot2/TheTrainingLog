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



        

