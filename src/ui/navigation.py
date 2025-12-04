import streamlit as st
from src.core.data_type_transform import flatten_day_to_dataframe
#--- Functions to navigate between screens ---
def nav_to(screen):
    st.session_state.current_screen = screen
    st.rerun()

def reset_to_home():
    st.session_state.selected_week = None
    st.session_state.selected_day = None
    nav_to('week_select')
    st.rerun()

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

def render_movements_and_sets(day_data: dict, key_label: str):
    st.data_editor(flatten_day_to_dataframe(day_data),
                   key=key_label, hide_index=True, use_container_width=True)




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