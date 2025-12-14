import streamlit as st
import pandas as pd

def append_desktop_builder_step1_edited_dfs():
    num_days = st.session_state.builder_num_days
    dfs = []
    for i in range(num_days):
       dfs.append(st.session_state[f'day_table_{i}'])

    df = pd.concat(dfs, ignore_index=True)
    #df = df.dropna()
    return df