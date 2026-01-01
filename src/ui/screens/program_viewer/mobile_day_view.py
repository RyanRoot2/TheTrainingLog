import streamlit as st
import pandas as pd
from src.backend.firestore import update_program_in_firestore # Assuming this import exists

def render_mobile_day_view():
    # 1. Setup Context
    week = st.session_state.program_viewer_mobile_selected_week
    day = st.session_state.program_viewer_mobile_selected_day
    
    st.header(f"Week {week} - Day {day}")
    
    # Access the master JSON from session state
    program_json = st.session_state.program_json
    
    # Target the specific day's data
    # Note: modifications to 'workout_data' here reference the object inside program_json
    workout_data = program_json["program"]["weeks"][f"week_{week}"][f"day_{day}"]

    # 2. Configuration Maps
    # DB Key -> UI Label
    column_config_map = {
        "set_number": "Set",
        "reps": "Reps",
        "weight": "Weight",
        "rpe_target": "RPE Target",
        "rir_target": "RIR Target",
        "set_range": "Set Range",
        "%_1rm": "% 1RM",
        "reps_completed": "Completed" # Added this just in case you track it
    }
    
    # UI Label -> DB Key (For saving back)
    reverse_column_map = {v: k for k, v in column_config_map.items()}

    # 3. Edit Buffer
    # We store the edited DataFrames here, keyed by the movement index
    edited_movements_buffer = {}

    # --- RENDER LOOP ---
    for i, movement in enumerate(workout_data["movements"]):
        with st.expander(f"{movement['exercise']}"):
            
            # A. Prepare Data
            # Handle potential empty sets list gracefully
            sets_data = movement.get("sets", [])
            df = pd.DataFrame(sets_data)
            
            if df.empty:
                st.info("No sets configured for this exercise.")
                continue

            # B. Filter & Rename for Display
            # Only show columns that actually exist in the data AND are in our config
            available_cols = [col for col in column_config_map.keys() if col in df.columns]
            df_display = df[available_cols].copy()
            
            # Rename for the UI
            df_display = df_display.rename(columns=column_config_map)

            # C. Render Editor
            # Unique Key is critical here (using exercise name + index)
            updated_df = st.data_editor(
                df_display, 
                hide_index=True, 
                use_container_width=True,
                key=f"editor_{movement['exercise']}_{i}"
            )

            # D. Capture Result
            edited_movements_buffer[i] = updated_df

    # --- SAVE LOGIC ---
    if st.button("Save Workout"):
        try:
            # 1. Process the Buffer
            for idx, df_edited in edited_movements_buffer.items():
                
                # Reverse rename: "Reps" -> "reps"
                df_clean = df_edited.rename(columns=reverse_column_map)
                
                # Convert numeric columns safely (optional but recommended)
                # This prevents "10" (string) from being saved when you want 10 (int)
                cols_to_numeric = ["reps", "weight", "set_number"]
                for col in cols_to_numeric:
                    if col in df_clean.columns:
                        df_clean[col] = pd.to_numeric(df_clean[col], errors='ignore')

                # Convert back to list of dicts
                new_sets_data = df_clean.to_dict('records')
                
                # Update the Session State JSON object directly
                # Since 'workout_data' is a reference to the inner dict of 'program_json',
                # updating it updates the main session_state object.
                workout_data["movements"][idx]["sets"] = new_sets_data

            # 2. Persist to Firestore
            # We save the entire updated program_json to the DB
            program_id = st.session_state.active_program_id 
            update_program_in_firestore(program_id, program_json)
            
            st.success("Workout saved successfully!")
            
            # 3. Refresh (Optional)
            # Useful if you want the "Save" button to reset or UI to acknowledge the sync
            # st.rerun()

        except Exception as e:
            st.error(f"An error occurred while saving: {e}")