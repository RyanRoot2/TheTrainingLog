import streamlit as st
import numpy as np
import pandas as pd

def initialise_desktop_builder_state(num_days):
    column_titles = ['Movement', 'Options']
    starting_rows = 8
    num_cols = len(column_titles)

    data = []
    for _ in range(starting_rows):
        data.append({'Movement': '', 'Options': []}) # Initialize with explicit empty list
    base_df = pd.DataFrame(data, columns=column_titles)
    
    # Explicitly ensure dtypes for robustness, though numpy with '' should handle it
    base_df = base_df.astype({'Movement': 'object', 'Options': 'object'})



    for i in range(num_days):
        if f'add_movement_day_{i}_state' not in st.session_state:
            st.session_state[f'add_movement_day_{i}_state'] = False
        if f'day_table_{i}' not in st.session_state:
            st.session_state[f'day_table_{i}'] = base_df.copy()


