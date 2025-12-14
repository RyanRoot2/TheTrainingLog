import numpy as np
import streamlit as st
import pandas as pd

def render_day_column(i):
    # Required local variables

    multiselect_options = [
        '% 1RM', 'RPE Target', 'RIR Target', 'Set Range',
    ]

    # Dataframe specifics
    column_titles = ['Movement', 'Options']
    starting_rows = 8
    data = []
    for _ in range(starting_rows):
        data.append({
            "Movement": "",
            "Options": []
        })
    df = pd.DataFrame(data, columns=column_titles)

    # Start of page
    st.write(f"Day {i+1}")
    
    # Data Editor
    edited_df = st.data_editor(
        df,
        hide_index=True,
        key=f'data_editor_day_{i}',
        num_rows='dynamic',
        column_config={
            "Movement": st.column_config.TextColumn(
                "Movement",
            ),
            "Options": st.column_config.MultiselectColumn(
                "Options",
                options=multiselect_options
            )
        }
    )

    st.session_state[f'day_table_{i}'] = edited_df

    st.write(st.session_state)

    st.write(df)

