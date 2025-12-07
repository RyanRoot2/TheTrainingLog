import streamlit as st
from src.utils.streamlit_temp_auth import check_st_authentication
from src.core.state import initialise_state


def show_login_button():
    # If the user is NOT logged in (st.user is not authenticated)
    if not st.user.is_logged_in:
        st.title("Secure App Demo")
        st.info("👋 Please log in to continue.")
        
        # Display the login button, which triggers the OIDC flow
        if st.button("Log in with Google"):
            st.login() 
        
        # Prevent the rest of the application from running
        st.stop()
show_login_button()

if st.button("Log out"):
    st.logout()
st.write(f"Hello, {st.user.name}!")

initialise_state()
st.info("👋 Hello!")
st.button("Go to next workout... TBC")











