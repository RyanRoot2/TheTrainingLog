import streamlit as st
from src.utils.streamlit_temp_auth import check_st_authentication
from src.core.state import initialise_state


check_st_authentication()
initialise_state()
st.write(st.session_state)

st.button("Go to next workout... TBC.")











