import streamlit as st
from src.backend.firestore import program

def render_mobile_day_view_tabs():
    weeks = program.get("weeks", [])
    if not weeks:
        st.info("No weeks available.")
        return

    tab_labels = [f"Week {i+1}" for i in range(len(weeks))]
    tabs = st.tabs(tab_labels)