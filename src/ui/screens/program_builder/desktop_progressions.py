import streamlit as st
import pandas as pd
from collections import defaultdict

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

def build_progression_df(options: tuple[str], df:pd.DataFrame) -> pd.DataFrame:
    base_cols = ['Movement']
    standard_cols = ['Sets', 'Reps']
    prog_df = df[base_cols].copy()
    for col in standard_cols:
        prog_df[col] = None
    for option in options:
        prog_df[option] = None
    
    return prog_df

def render_day_progressions(day, day_df):
    """
    Input day_df = dfs_by_day[0] which is a dict(options: df)
    Where options is still a tuple ("% 1RM", ...)

    This is the key rendering component.
    May want to switch to tabs or remove it and use subheaders to keep everything on the page.
    """
    with st.expander(f'Day {day+1}', expanded=True):
        for options, df in day_df.items():
            prog_df = build_progression_df(options, df)
            st.data_editor(
                data=prog_df,
                hide_index=True,
                key=f"program_bulder_desktop_progressions_day_{day}_{'_'.join(options)}"
            )


def render_desktop_progressions():
    st.success("Great success!")

    program_builder_data = st.session_state.program_builder_data
    st.write(program_builder_data)
    grouped_dfs = split_by_config(program_builder_data)
    dfs_by_day = regroup_by_day(grouped_dfs)

    for day in sorted(dfs_by_day.keys()):
        render_day_progressions(day, dfs_by_day[day])
