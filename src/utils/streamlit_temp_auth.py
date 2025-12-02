import streamlit as st

def streamlith_auth():
    # Get password from Streamlit Secrets
    PASSWORD = st.secrets["credentials"]["password"]
    # Ask user for password
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if not st.session_state.authenticated:
        password_input = st.text_input("Enter password", type="password")
        if password_input == PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.warning("Incorrect password")
            st.stop()  # Stops execution for wrong password


def check_st_authentication():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if not st.session_state.authenticated:
        streamlith_auth()