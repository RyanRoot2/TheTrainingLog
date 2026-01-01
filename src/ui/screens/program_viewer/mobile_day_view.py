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
    # Workout Data format {"movements": [ {exercise: str, sets: [set num, reps, weight, etc - all str ] }, ... ] }
    workout_data = program_json["program"]["weeks"][f"week_{week}"][f"day_{day}"]

    # Expander
    for movement in workout_data["movements"]:
        with st.expander(f"{movement['exercise']}"):
            df = pd.DataFrame(movement["sets"])
            # Columns to show
            display_columns = ["set_number", "reps", "weight", "rpe_target", "rir_target", "set_range", "%_1rm"]
            df_display = df[[col for col in display_columns if col in df.columns]]
            df_display = df_display.rename(columns={
                "set_number": "Set",
                "reps": "Reps",
                "weight": "Weight",
                "rpe_target": "RPE Target",
                "rir_target": "RIR Target",
                "set_range": "Set Range",
                "%_1rm": "% 1RM"
            })
            st.data_editor(df_display, hide_index=True, use_container_width=True)

    # Save Button
    if st.button("Save Workout"):
        st.success("Workout saved!") # Call backend save function here