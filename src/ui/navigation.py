import streamlit as st
#--- Functions to navigate between screens ---
def nav_to(screen):
    st.session_state.current_screen = screen
    st.rerun()

def reset_to_home():
    st.session_state.selected_week = None
    st.session_state.selected_day = None
    nav_to('week_select')
    st.rerun()

def render_week_grid_mobile(program: dict, number_of_columns: int = 3):
    weeks_keys = list(program["weeks"].keys())
    num_weeks = len(weeks_keys)
    weeks = range(1,num_weeks + 1)  # Example: Weeks 1 to 12
    cols = st.columns(number_of_columns)
    for idx, week_num in enumerate(weeks):
        col = cols[idx % number_of_columns] # 3 cols
        with col:
            if st.button(f"Week {week_num}", key=f"week_{week_num}_button", use_container_width=True):
                st.session_state.selected_week = week_num
                nav_to('day_select')
                
def render_day_grid_mobile(program_week: dict, number_of_columns: int = 1):
    days_keys = list(program_week.keys())
    days = range(1, len(days_keys) + 1)  # Example:
    cols = st.columns(number_of_columns)
    for idx, day_num in enumerate(days):
        col = cols[idx % number_of_columns] # 1 col
        with col:
            if st.button(f"Day {day_num}", key=f"day_{day_num}_button", use_container_width=True):
                st.session_state.selected_day = day_num
                nav_to('day_view')



def render_grid(dict: dict, number_of_columns: int, nav_to: str):
    pass




"""
# Handle selected week's screen, days selection
st.subheader(f"Selected Week: {st.session_state.selected_week}")
days_grid = range(1,6)  # Example: Days 1 to 5
for day_num in days_grid:
    if st.button(f"Day {day_num}", key=f"day_{day_num}", use_container_width=True):
        st.session_state.selected_day = day_num
        nav_to('day_view')

# Handle selected day's screen, display movements and sets
st.subheader(f"Selected Day: {st.session_state.selected_day}")
week_key = f"week_{st.session_state.selected_week}"
day_key = f"day_{st.session_state.selected_day}"
if 'selected_week' in st.session_state and 'selected_day' in st.session_state:
    movements = program["weeks"][week_key][day_key]["movements"]
    for movement_index, movement in enumerate(movements):
        st.markdown(f"**{movement['Name']}**")
        table = []
        for set_index, set in enumerate(movement["sets"], start=1):
            table.append({
                "Set": set_index,
                "Rep Range": f"{set['Reps_Target'][0]} - {set['Reps_Target'][1]}",
                "Weight" : set["Weight"],
                "Reps": set["Reps_Completed"]
            })   
        df = pd.DataFrame(table)
        num_rows_df = len(df)
        row_height = 35  # Approximate height per row in pixels
        total_height = row_height * num_rows_df + 40  # Additional space for header
        edited_df = st.data_editor(df,
                                key=f"week{st.session_state.selected_week}_day{st.session_state.selected_day}_movement{movement_index}",
                                hide_index=True,
                                use_container_width=True,
                                height=total_height
                                )
                            """