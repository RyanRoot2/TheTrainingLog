import streamlit as st
from src.core.state import nav_to

def render_grid(item_name: str, dict: dict, number_of_columns: int, screen_to_nav_to: str):
    keys = list(dict.keys())
    num_items = len(keys)
    items = range(1,num_items + 1)  # Example: Weeks 1 to 12, Days 1 to 5
    cols = st.columns(number_of_columns)
    for idx, item_num in enumerate(items):
        col = cols[idx % number_of_columns]
        with col:
            if st.button(f"{item_name} {item_num}", key=f"{item_name.lower()}_{item_num}_button", use_container_width=True):
                if item_name == "Week":
                    st.session_state.selected_week = item_num
                elif item_name == "Day":
                    st.session_state.selected_day = item_num
                nav_to(screen_to_nav_to)