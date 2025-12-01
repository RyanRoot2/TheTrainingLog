import streamlit as st
import json
import pandas as pd
from google.cloud import firestore

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




import streamlit as st
from browser_detection import browser_detection_engine

value = browser_detection_engine()
st.header(value)






# --- CONFIGURATION (MUST MATCH YOUR SETUP) ---
CUSTOM_DB_NAME = 'training-log' 
COLLECTION_NAME = 'activePrograms'
DOCUMENT_ID = 'workout_v1_0'
# ---------------------------------------------
# 1. Initialize the Secure Connection Client
@st.cache_resource
def get_firestore_client():
    # Pass the database name explicitly for custom-named databases
    return firestore.Client.from_service_account_info(
        st.secrets["firestore"],
        database=CUSTOM_DB_NAME
    )

db = get_firestore_client()

# 2. Load the JSON Data into a Dictionary
# Caching is crucial here: prevents a database read on every app interaction
@st.cache_data(ttl=3600) # Re-read data from Firestore only once every hour
def load_workout_json():
    try:
        doc_ref = db.collection(COLLECTION_NAME).document(DOCUMENT_ID)
        doc = doc_ref.get()
        
        if doc.exists:
            return doc.to_dict()
        else:
            st.error(f"Error: Document {DOCUMENT_ID} not found in Firestore.")
            return None
    except Exception as e:
        st.error(f"Failed to load data from Firestore: {e}")
        return None

program = load_workout_json() 

if program is None:
    st.stop() # Stop execution if data couldn't be loaded





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

                    for movement_index, movement in enumerate(movements):
                        st.markdown(f"**{movement["Name"]}**")
                        table = []
                        for set_index, set in enumerate(movement["sets"], start=1):
                            table.append({
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
                                                key=f"week{week_index_start + count + 1}_day{day+1}_movement{movement_index}",
                                                hide_index=True,
                                                use_container_width=True,
                                                height=total_height
                                                )

                        for _, row in edited_df.iterrows():
                            set_number = row["Set"]
                            set_index = int(set_number) - 1
                            movement["sets"][set_index]["Reps_Completed"] = row["Reps"]
                            movement["sets"][set_index]["Weight"] = row["Weight"]
                        doc_ref = db.collection(COLLECTION_NAME).document(DOCUMENT_ID)
                        doc_ref.set(program)
            count += 1





