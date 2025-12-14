import streamlit as st
import pandas as pd

def render_day_column(i):
    # Required local variables
    table_key = f'day_table_{i}'
    active_form_key = f'add_movement_day_{i}_state'
    multiselect_options = [
        'Sets', 'Reps', '% 1RM', 'RPE Target', 'RIR Target', 'Set Range',
    ]

    # Dataframe specifics
    column_titles = ['Movement Name', 'Configurable Fields']
    table_data = st.session_state[table_key]
    df = pd.DataFrame(data=table_data, columns=column_titles)

    # Start of page
    st.write(f"Day {i+1}")
    
    # Data Editor
    edited_df = st.data_editor(
        table_data,
        hide_index=True,
        key=f'data_editor_day_{i}',
        num_rows='dynamic',
        column_config={
            "Movement": st.column_config.TextColumn(
                "Movement",
                width="medium",
                required=True
            ),
            "Config": st.column_config.SelectboxColumn(
                "Config",
                options=multiselect_options,
                required=True
            )
        }
    )

    # Handle edits to the editor immediately
    if not edited_df == table_data:
        st.session_state[table_key] = edited_df
        st.rerun()


    if st.button(label=f"Add Movement", key=f"add_movement_btn_day_{i}"):
        st.session_state[active_form_key] = True

    if st.session_state[active_form_key] is True:
        with st.form(key=f"add_movements_day_{i}_form", clear_on_submit=False):
            col1, col2 = st.columns(2)
            with col1:
                movement_name = st.text_input(label="Movement Name", key=f"movement_name_input_{i}")
            with col2:
                progression_mode = st.multiselect("Progression Mode", options=multiselect_options,
                                                  key=f"progression_mode_input_{i}")
            submitted = st.form_submit_button("Confirm")
            if submitted:
                st.session_state[f'day_table_{i}'].append([movement_name, progression_mode])
                st.session_state[active_form_key] = False
                st.rerun()