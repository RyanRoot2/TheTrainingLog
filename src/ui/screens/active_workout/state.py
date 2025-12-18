        
    # --- UI NAVIGATION STATE ---
    # Tracks the user's current view (e.g., 'week_select', 'workout_view')
    if 'current_screen' not in st.session_state:
        st.session_state.current_screen = None
        # Possible values:
        # 'week_select' - User is selecting a week
        # 'day_select'  - User is selecting a day within the week
        # 'day_view'    - User is viewing the day's workout details
        
    # Stores the selected week number (e.g., 1, 5, 12)
    if 'selected_week' not in st.session_state:
        st.session_state.selected_week = None
        
    # Stores the selected day number (e.g., 1, 3, 5)
    if 'selected_day' not in st.session_state:
        st.session_state.selected_day = None
        
    # --- DATA STATE (for later) ---
    # Tracks the master dataframe for editing
    if 'master_df' not in st.session_state:
        st.session_state.master_df = None