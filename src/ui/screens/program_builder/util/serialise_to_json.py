import streamlit as st
import re

def serialise_to_json(): 
    """
    Pre-shapes the JSON based on num_weeks and num_days, 
    then populates it with movement data from session_state.
    """
    # 1. Get dimensions from session_state
    num_weeks = st.session_state.get('program_builder_desktop_num_weeks', 0)
    num_days = st.session_state.get('program_builder_desktop_num_days', 0)
    
    # 2. Pre-shape the skeleton
    # This ensures "Day 3" exists even if it's empty
    program_json = {"weeks": {}}
    for w in range(1, num_weeks + 1):
        week_key = f"week_{w}"
        program_json["weeks"][week_key] = {}
        for d in range(1, num_days + 1):
            program_json["weeks"][week_key][f"day_{d}"] = {"movements": []}

    # 3. Identify and process the data editor DataFrames
    # Pattern matches your storage key: program_bulder_desktop_progressions_day_X_...
    key_pattern = re.compile(r"program_builder_desktop_progressions_day_(\d+)")
    
    relevant_keys = [
        k for k in st.session_state.keys()
        # Startswith allows theloop to capture the different _{options} in the full key name
        if k.startswith("program_builder_desktop_progressions_day_")
    ]

    for key in relevant_keys:
        # Get match object for the key
        match = key_pattern.search(key)
        if not match:
            continue
        
        # Use the .group attribute to extract the day the key is referring to
        day_index = int(match.group(1))
        day_key = f"day_{day_index + 1}"

        # Get the DataFrame result from the editor
        df = st.session_state[key]
        
        # 4. Map the Wide DataFrame into the Pre-shaped Shell
        for w in range(1, num_weeks + 1):
            week_key = f"week_{w}"
            
            for _, row in df.iterrows():
                movement_name = row.get('Movement')
                if not movement_name or movement_name == "":
                    continue
                
                # Get number of sets and reps for the movement entry
                num_sets = row.get(f"W{w} Sets", 0)
                num_reps = row.get(f"W{w} Reps", 0)
                assert num_sets is not None, "Sets cannot be None"

                # Generate a list of set dictionaries
                sets_list = []
                for s in range(int(1, num_sets+1)):
                    sets_list.append({
                        "set_number": s,
                        "reps": num_reps,
                        "weight": None,
                        "completed": False
                    })

                # Build the movement object
                movement_entry = {
                    "exercise": movement_name,
                    "sets": sets_list
                }

                # Dynamically add RPE, % 1RM, etc.
                prefix = f"W{w} "
                for col in df.columns:
                    if col.startswith(prefix):
                        metric_name = col[len(prefix):]
                        if metric_name not in ["Sets", "Reps"]:
                            clean_key = metric_name.lower().replace(" ", "_")
                            # Add the key to every set
                            for s in range(len(sets_list)):
                                sets_list[s][clean_key] = row[col]

                # Append to the pre-existing day list
                program_json["weeks"][week_key][day_key]["movements"].append(movement_entry)

    return program_json