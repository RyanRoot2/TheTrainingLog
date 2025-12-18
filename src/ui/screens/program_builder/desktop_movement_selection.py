import streamlit as st
import pandas as pd


# from src.ui.components.desktop_program_builder_column import render_day_column
from src.ui.screens.program_builder.components.day_column import render_day_column


def append_desktop_builder_movement_selection():
    num_days = st.session_state.program_builder_desktop_num_days
    dfs = []
    for i in range(num_days):
       dfs.append(st.session_state[f'program_builder_desktop_movement_selection_data_{i}'])

    df = pd.concat(dfs, ignore_index=True)
    #df = df.dropna()
    return df


def render_desktop_movement_selection(num_days):
    days = st.columns(num_days)

    # Render each column
    for i, col in enumerate(days):
        with col:
            render_day_column(i)

    if st.button("Configure Sets, Reps, and Progressions -->"):
        program_builder_data = append_desktop_builder_movement_selection()
        st.session_state.program_builder_data = program_builder_data
        st.session_state.program_builder_desktop_screen = 'progressions'
        st.rerun()
        


