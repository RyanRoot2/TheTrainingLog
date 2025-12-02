import streamlit as st
from src.utils.streamlit_temp_auth import check_st_authentication
from src.core.state import initialise_state


check_st_authentication()
initialise_state()
st.write(st.session_state)

st.button("Go to next workout... TBC")



"""



# def get_firestore_client():

db = get_firestore_client()

 # Re-read data from Firestore only once every hour
# def load_workout_json():
program = load_workout_json() 

if program is None:
    st.stop() # Stop execution if data couldn't be loaded



# styling moved to styles.py



"""










