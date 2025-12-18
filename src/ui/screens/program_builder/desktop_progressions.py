import streamlit as st
import pandas as pd

def render_desktop_progressions():
    st.success("Great success!")

    program_builder_data = st.session_state.program_builder_data

    st.dataframe(program_builder_data)