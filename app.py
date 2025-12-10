import streamlit as st
from src.backend.firebase_init import initialise_firebase_admin
from src.core.state import initialise_state
from src.core.login import enforce_login

initialise_firebase_admin()
enforce_login()
initialise_state()



st.success(f"Welcome")
st.info("👋 Under Construction!")


# =======
# Current Program / Program Selection flow example
# =======
if 'current_program' not in st.session_state:
    st.session_state.current_program = 'None'

@st.dialog("Choose Program")
def choose_program():
    selected_program = st.selectbox('Label', ["5/3/1", "Upper Lower Arms 5x", "PPL 6x"])
    if st.button("Save"):
        st.session_state.current_program = selected_program
        st.rerun()
if st.button(f"Current Program: {st.session_state.current_program}"):
    choose_program()



# =======
# Program Templates / User's available programs
# =======
option_dict = {
    "5/3/1": "Jim Wenderl's 5/3/1 with First Set Last",
    "Upper Lower Arms & Shoulders 5x": "Upper Lower, Upper Lower, and a dedicated day for Arms and Shoulders",
    "PPL 6x": "Classic Push Pull Legs 6 days per week"
}
with st.expander(label='Program Templates'):
    with st.expander(label='Filters'):
        filters = ['3x', '4x', '5x', '6x', 'My Templates Only', 'Strength', 'Hypertrophy',
                   'Weekly Periodisation', 'Block Periodisation', 'Linear Progression']
        for filter in filters:
            st.checkbox(filter)
    option = st.selectbox(label="Programs", options=("5/3/1", "Upper Lower Arms & Shoulders 5x", "PPL 6x"))
    st.write(f"{option_dict[option]}")


# =======
# Logout
# =======
if st.button("Log out"):
    st.logout()













