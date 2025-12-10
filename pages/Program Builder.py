import streamlit as st
import pandas as pd

st.success("Program Builder")
st.set_page_config(layout="wide")


def get_program_dimensions():
    st.subheader("Define Program Structure")
    with st.form("program_structure_form", clear_on_submit=False):
        col1, col2 = st.columns(2)

        with col1:
            num_weeks = st.number_input('Number of Weeks', min_value=1, max_value=12, value=1, key="num_weeks")
        with col2:
            num_days = st.number_input('Number of Days', min_value=1, max_value=7, value=4, key='num_days')

        submitted = st.form_submit_button("Go to next step")

        if submitted:
            st.session_state['builder_num_weeks'] = num_weeks
            st.session_state['builder_num_days'] = num_days
            st.rerun()


def render_program_builder_tabs():
    mobile, desktop, settings = st.tabs([
        "Mobile",
        "Desktop",
        "Settings"
    ])

    with mobile:
        st.info("Mobile")

    with desktop:
        if 'builder_num_weeks' not in st.session_state:
            get_program_dimensions()
            st.stop()
        num_days = st.session_state.builder_num_days
        days = st.columns(num_days)
        st.write(st.session_state)
        for i in range(num_days):
            key = f'add_movement_day_{i}'
            if key not in st.session_state:
                st.session_state[key] = None
                st.write(f"Set value for {key}: {st.session_state[key]}")
            with days[i]:
                if f'day_table_{i}' not in st.session_state:
                    st.session_state[f'day_table_{i}'] = []
                st.dataframe(st.session_state[f'day_table_{i}'])
                st.write(st.session_state[f'day_table_{i}'])
                st.write(f"Day {i+1}")
                if st.button(label=f"Add Movements for Day {i}", key=f"add_movements_day_{i}_button"):
                    st.session_state[key] = True
                    st.write(f"Set session state for {key} to True")
                if st.session_state[key]:
                    with st.form(key=f"add_movements_day_{i}_form"):
                        col1, col2 = st.columns(2)
                        with col1:
                            movement_name = st.text_input(label="Movement Name", key=f"movement_name_input_{i}")
                        with col2:
                            progression_mode = st.selectbox("Progression Mode", options=['N/A'], key=f"progression_mode_input_{i}")
                        submitted = st.form_submit_button("Confirm")
                        if submitted:
                            st.session_state[f'day_table_{i}'].append([movement_name, progression_mode])
                            st.session_state[key] = False
                            st.rerun()




render_program_builder_tabs()