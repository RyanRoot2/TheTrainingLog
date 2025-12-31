import streamlit as st
from src.backend.firebase_init import initialise_firebase_admin
from src.core.state import initialise_state
from src.core.login import enforce_login
#from src.utils.device_detection import DEVICE_INFO

initialise_firebase_admin()
enforce_login()
initialise_state()
st.write(st.session_state)
#st.write(DEVICE_INFO)

#if DEVICE_INFO['isDesktop'] is True:
#    st.write("Use to update settings.")



st.success(f"Welcome")
st.info("👋 Under Construction!")



# =======
# Logout
# =======
st.write("------------------")
if st.button("Log out"):
    st.logout()


