import pandas as pd
from typing import Dict, Any, List

def flatten_day_to_dataframe(day_data: Dict[str, Any]) -> pd.DataFrame:
    """Flattens the movements and sets of a day's workout into a single DataFrame."""
    all_sets = []
    for movement in day_data.get("movements", []):
        movement_name  = movement.get("Name", "")
        for set_index, set_data in enumerate(movement.get("sets", []), start=1):
            row = {
                "Movement": movement_name,
                "Set": set_index,
                "Rep Range": f"{set_data['Reps_Target'][0]} - {set_data['Reps_Target'][1]}",
                "Weight": set_data.get("Weight", 0),
                "Reps": set_data.get("Reps_Completed", 0)
            }
            all_sets.append(row)
    return pd.DataFrame(all_sets)


def update_program_json(program: dict, edited_df: pd.DataFrame, week_num: int, day_num: int):
    week_key = f"week_{week_num}"
    day_key = f"day_{day_num}"

    try:
        movements = program["weeks"][week_key][day_key]["movements"]
    except KeyError as e:
        print(f"Error accessing movements in JSON structure: {e}")
        return

    df_index = 0

    for movement in movements:
        for set_number, set_data in enumerate(movement["sets"]):
            if df_index < len(edited_df):
                row = edited_df.iloc[df_index]
                movement["sets"][set_number]['Reps_Completed'] = int(row.get('Reps', set_data['Reps_Completed']))
                movement["sets"][set_number]['Weight'] = float(row.get('Weight', set_data['Weight']))

                df_index += 1
            else:
                print("Warning: Edited DataFrame ran out of rows. JSON is expecting more input")
                break