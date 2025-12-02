import streamlit as st
from browser_detection import browser_detection_engine

value = browser_detection_engine()
st.header(value)