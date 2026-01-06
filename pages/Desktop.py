import streamlit as st
from src.core.login import enforce_login
st.set_page_config(layout="wide")
enforce_login() # Auth check on every page

st.info("👋 Desktop version under construction! Check out the mobile page!")