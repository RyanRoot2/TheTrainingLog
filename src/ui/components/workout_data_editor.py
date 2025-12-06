import streamlit as st
from src.core.data_transform import flatten_day_to_dataframe

def render_movements_and_sets(day_data: dict, key_label: str):
    
    df = flatten_day_to_dataframe(day_data)
    num_rows = len(df)
    height = 38*num_rows
    
    # 1. Define internal columns to hide
    excluded_columns = {"Set"} 

    # 2. Define the desired order for the MAIN workout data columns
    # This list only needs to contain the columns you care about the order of.
    display_priority = ["Movement", "Rep Range", "Weight", "RPE", "Reps", "Notes"] 
    
    # 3. Get all available columns after excluding hidden/internal ones
    available_columns = set(df.columns) - excluded_columns
    
    # 4. Create the final list for column_order:
    #    Iterate through the 'display_priority' list and only keep columns
    #    that exist in the 'available_columns' set.
    visible_columns_in_order = [
        col for col in display_priority 
        if col in available_columns
    ]
    
    # Check for any new, unlisted columns (e.g., 'Tempo') and append them
    # This makes the solution completely robust to new column additions.
    # We convert both to sets to find the difference.
    unprioritized_columns = list(available_columns - set(visible_columns_in_order))
    
    # Final column list combines the prioritized ones and any new ones
    final_column_order = visible_columns_in_order + unprioritized_columns

    
    # 5. Configuration (still needed for disabling Rep Range)
    config = {
        "Set": st.column_config.Column(
            label="Set",
            disabled=True
        ),
        "Rep Range": st.column_config.Column(
            label="Target",
            disabled=False,
            width="small"
        ),
            "Weight": st.column_config.Column(
            label="Weight",
            disabled=False,
            width=50
        ),
            "Reps": st.column_config.Column(
            label="Reps",
            disabled=False,
            width=50
        ),
            "Movement": st.column_config.Column(
            label="Movement",
            disabled=False,
            width="medium"
        )
    }

    edited_df = st.data_editor(
        data=df,
        height=height,
        column_config=config,
        column_order=final_column_order,
        key=key_label,
        hide_index=True,
        use_container_width=True
    )
    
    return edited_df