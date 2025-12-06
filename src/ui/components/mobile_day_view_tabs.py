import streamlit as st
from src.backend.firestore import program

def render_mobile_day_view_week_navigation():
    weeks = list(program.get("weeks", {}).keys())
    sorted_week_keys = sorted(weeks, key=lambda k: int(k.split('_')[1]))
    
    # Create a mapping for display names
    # Display: "Week 1" -> Returns: 1
    options = [int(k.split('_')[1]) for k in sorted_week_keys]
    
    # This renders a horizontal bar of buttons
    selected = st.segmented_control(
        "Weeks",
        options=options,
        format_func=lambda x: f"Week {x}", # Makes the button say "Week 1"
        default=st.session_state.selected_week,
        key="nav_pill_selection_week"
    )

    # Logic to update state immediately
    if selected != st.session_state.selected_week:
        st.session_state.selected_week = selected
        st.rerun()

def render_mobile_day_view_day_navigation():
    selected_week = st.session_state.selected_week
    all_keys = list(program["weeks"].get(f"week_{selected_week}", {}).keys())
    days = [k for k in all_keys if k.startswith("day_")]
    sorted_days_keys = sorted(days, key=lambda k: int(k.split('_')[1]))
    
    # Create a mapping for display names
    # Display: "Week 1" -> Returns: 1
    options = [int(k.split('_')[1]) for k in sorted_days_keys]
    
    # This renders a horizontal bar of buttons
    selected = st.segmented_control(
        "Days",
        options,
        format_func=lambda x: f"Day {x}", # Makes the button say "Week 1"
        default=st.session_state.selected_day,
        key="nav_pill_selection_day"
    )

    # Logic to update state immediately
    if selected != st.session_state.selected_day:
        st.session_state.selected_day = selected
        st.rerun()