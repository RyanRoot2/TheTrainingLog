import streamlit as st
import json
import pandas as pd

# Get the password from Streamlit Secrets
PASSWORD = st.secrets["credentials"]["password"]
# Ask user for password
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if not st.session_state.authenticated:
    password_input = st.text_input("Enter password", type="password")
    if password_input == PASSWORD:
        st.session_state.authenticated = True
        st.rerun()
    else:
        st.warning("Incorrect password")
        st.stop()  # Stops execution for wrong password

st.set_page_config(layout="wide")

st.markdown("""
<style>
.stMainBlockContainer {
    padding-left: 0rem;
    padding-right: 0rem;
    padding-top: 2rem;
    padding-bottom: 2rem;
}
.stAppHeader {
    background-color: rgba(255, 255, 255, 0.0);
    visibility: visible;
}
</style>
""", unsafe_allow_html=True)

with open('programs/mass_impact.json') as f:
    program = json.load(f)

weeks = list(program["weeks"].keys())  # ["week_1", "week_2", ...]
num_weeks = len(weeks)
num_rows = (num_weeks + 3) // 4  # Calculate number of rows needed for 4 columns
days = 5

for row in range(num_rows):
    expander = st.expander(f"Phase {row+1}", expanded=False, icon=None, width="stretch")
    with expander:
        cols = st.columns(4)
        week_index_start = row * 4
        count = 0
        for col in cols:
            with col:
                st.header(f"Week {week_index_start + count + 1}")
                for day in range(days):
                    st.subheader(f"Day {day + 1}")

                    movements = program["weeks"][f"week_{week_index_start + count + 1}"][f"day_{day + 1}"]["movements"]
                    table = []
                    for movement in movements:
                        for set_index, set in enumerate(movement["sets"], start=1):
                            table.append({
                                "Movement": movement["Name"],
                                "Set": set_index,
                                "Rep Range": f"{set["Reps_Target"][0]} - {set["Reps_Target"][1]}",
                                "Weight" : set["Weight"],
                                "Reps": set["Reps_Completed"]
                            })   
                    df = pd.DataFrame(table)
                    num_rows_df = len(df)
                    row_height = 35  # Approximate height per row in pixels
                    total_height = row_height * num_rows_df + 40  # Additional space for header
                    edited_df = st.data_editor(df,
                                               key=f"week{week_index_start + count + 1}_day{day+1}",
                                               hide_index=True,
                                               use_container_width=True,
                                               height=total_height
                                               )
                    for movement in movements:
                        movement_rows = edited_df[edited_df["Movement"] == movement["Name"]]
                        for _, row in movement_rows.iterrows():
                            set_number = row["Set"]
                            set_index = int(set_number) - 1
                            movement["sets"][set_index]["Reps_Completed"] = row["Reps"]
                            movement["sets"][set_index]["Weight"] = row["Weight"]
                        with open("programs/mass_impact.json", "w") as f:
                            json.dump(program, f, indent=4)
            count += 1





