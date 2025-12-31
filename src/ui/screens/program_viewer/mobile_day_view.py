import random
import streamlit as st
import pandas as pd


# Update after fixing the program creation methods to actually create the sets list
# Consider how the program json is actually transferred... should it use the cached resource or add it to session state?

def render_mobile_day_view():
    # Week and Day of Program
    week = st.session_state.program_viewer_mobile_selected_week
    day = st.session_state.program_viewer_mobile_selected_day
    # Header
    st.header(f"Week {week} - Day {day}")
    # This day's workout data
    program_json = st.session_state.program_json
    workout_data = program_json["program"]["weeks"][f"week_{week}"][f"day_{day}"]

    # Expander
    for movement in workout_data["movements"]:
        with st.expander(f"{movement['exercise']}"):

            num_sets = int(movement.get("sets"))
            
            df = pd.DataFrame([movement])

            df_repeated = df.loc[df.index.repeat(num_sets)].reset_index(drop=True)

            df_repeated.insert(0, "Set", range(1, num_sets + 1))
            df_repeated["Set"] = df_repeated["Set"].astype(str)
            df_repeated = df_repeated.rename(columns={"reps": "Reps", "weight": "Weight"})
            st.data_editor(df_repeated[["Set", "Reps", "Weight"]], hide_index=True)

    # Save Button
    if st.button("Save Workout"):
        st.success("Workout saved!") # Call backend save function here