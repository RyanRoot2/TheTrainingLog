import streamlit as st
from src.core.data_transform import flatten_day_to_dataframe

def render_movements_and_sets(day_data: dict, key_label: str):
    st.data_editor(flatten_day_to_dataframe(day_data),
                   key=key_label, hide_index=True, use_container_width=True)