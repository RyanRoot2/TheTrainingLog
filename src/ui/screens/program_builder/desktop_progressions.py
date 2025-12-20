import streamlit as st
import pandas as pd
from collections import defaultdict
from src.ui.screens.program_builder.util.serialise_to_json import serialise_to_json
from src.ui.screens.program_builder.state import clear_program_builder_state
from src.core.save_program_to_firestore import save_program_template_to_firestore

def split_by_config(program_builder_data: pd.DataFrame) -> dict[tuple, pd.DataFrame]:
    """
    Returns:
    {
    ((options), 0): df,
    ((options), 1): df
    }
    """
    df = program_builder_data.copy()
    df['_config_key'] = df['Options'].apply(
        lambda x: tuple(sorted(x)) if isinstance(x, list) else tuple()
    )

    grouped_dfs = {}

    # Key is a tuple of options, day (tuple, int)
    for key, group in df.groupby(['_config_key', 'day']):
        grouped_dfs[key] = group.drop(columns='_config_key').reset_index(drop=True)
    
    return grouped_dfs

def regroup_by_day(grouped_dfs):
    """
    Returns:
    {
    0: {options: df},
    1: {options: df}
    }
    """
    dfs_by_day = defaultdict(dict)

    # (options, day) is the key from the groupby
    for (options, day), df in grouped_dfs.items():
        dfs_by_day[day][options] = df

    return dfs_by_day

def build_progression_df(options: tuple[str], df:pd.DataFrame, num_weeks: int) -> pd.DataFrame:
    # Start with the Movement column
    prog_df = df[['Movement']].copy().reset_index(drop=True)
    # Create list of columns for inputs
    configurable_columns = ['Sets', 'Reps'] + sorted(list(options))
    # Create config columns in df for each week
    for week in range(1, num_weeks+1):
        for col in configurable_columns:
            col_name = f"W{week} {col}"
            prog_df[col_name] = ""
    
    return prog_df

def render_day_progressions(day, day_df):
    """
    Input day_df = dfs_by_day[0] which is a dict(options: df)
    Where options is still a tuple ("% 1RM", ...)

    This is the key rendering component.
    May want to switch to tabs or remove it and use subheaders to keep everything on the page.
    """
    num_weeks = st.session_state.program_builder_desktop_num_weeks
    st.subheader(f"Day {day+1}")
    # Sort the options so that data editors with more options are shown first
    sorted_day_dfs = sorted(day_df.items(), key=lambda x: len(x[0]), reverse=True)
    for options, df in sorted_day_dfs:
        prog_df = build_progression_df(options, df, num_weeks)

        # --- FREEZE LOGIC START ---
        column_configuration = {
            "Movement": st.column_config.TextColumn(
                "Movement",
                pinned=True     # Pins the column to the left during horizontal scroll
            )
        }
        # --- FREEZE LOGIC END ---

        edited_df = st.data_editor(
            data=prog_df,
            hide_index=True,
            column_config=column_configuration,
            key=f"st_data_editor_{day}_{'_'.join(options)}"
        )

        st.session_state[f"program_builder_desktop_progressions_day_{day}_{'_'.join(options)}"] = edited_df

@st.dialog("Success!")
def show_success_modal():
    st.write("Your program has been saved to Firestore.")
    if st.button("Back to Dashboard"):
        del st.session_state.show_success_dialog
        # CLEAR STATE HERE, inside the dialog interaction
        clear_program_builder_state() 
        st.switch_page('app.py')

def render_desktop_progressions():
    if st.session_state.get("show_success_dialog"):
        show_success_modal()

    program_builder_data = st.session_state.program_builder_data
    grouped_dfs = split_by_config(program_builder_data)
    dfs_by_day = regroup_by_day(grouped_dfs)
    
    for day in sorted(dfs_by_day.keys()):
        render_day_progressions(day, dfs_by_day[day])

    if st.button("Save Program -->"):
        json = serialise_to_json()
        save_program_template_to_firestore(program_data=json, template_name="My First Template")
        st.session_state.show_success_dialog = True
        st.rerun()
