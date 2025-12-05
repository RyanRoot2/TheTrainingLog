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