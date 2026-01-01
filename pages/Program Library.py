import streamlit as st
from src.core.login import enforce_login
from src.core.state import initialise_state
from src.backend.firestore import get_all_user_templates
from src.backend.firestore import copy_to_started_and_return_id
from src.backend.firestore import set_active_program_id
from src.backend.firestore import load_active_program_json



st.set_page_config(layout="wide")
enforce_login() # Auth check on every page
initialise_state() # Initialises app-level state to prevent deep-link crashes

st.header("Program Library")

# =========================

templates = get_all_user_templates()

if not templates:
    st.info("No program templates available at this time. Redirect to Program Builder here...")
    
for template in templates:
    with st.expander(template["template_name"]):
        #st.write(template["description"]) Add description to the program builder
        st.write(f"Program Length: {template["stats"]["weeks"]} Weeks, Days per Week: {template["stats"]["days_per_week"]}")
        if st.button(f"More Info", key=f"more_info_{template['id']}"):
            st.info("Coming Soon!")

        if st.button("Start Program", key=f"start_program_{template['id']}"):
            template_id = template["id"] # Correctly uses a string
            new_program_id = copy_to_started_and_return_id(template_id)
            set_active_program_id(new_program_id)
            load_active_program_json.clear()
            if "program_json" in st.session_state:
                st.session_state.program_json = None
            st.success(f"Started new program from template '{template['template_name']}'! Active program set.")
            # Function here to copy program template into the user_started_programs and set the active program to that copy's ID