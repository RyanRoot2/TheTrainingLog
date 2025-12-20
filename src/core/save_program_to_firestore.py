import streamlit as st
import datetime
from src.backend.firestore import get_firestore_client

def save_program_template_to_firestore(program_data, template_name="Untitled Program"):
    """
    Saves the serialized program JSON using the global cached Firestore client.
    """
    try:
        # 1. Access your existing cached client
        # It's best practice to call the function again; @st.cache_resource 
        # ensures it just returns the existing instance instantly.
        db = get_firestore_client()
        
        user_uid = st.session_state.get("user_uid")
        if not user_uid:
            st.error("Authentication Error: No User UID found.")
            return False

        # 2. Path: users -> {user_uid} -> user_program_templates
        # We use .document() to create a new doc with an auto-generated ID
        doc_ref = db.collection("users").document(user_uid).collection("user_program_templates").document()

        # 3. Enrich data with metadata for easier querying later
        payload = {
            "template_name": template_name,
            "created_at": datetime.datetime.now(datetime.timezone.utc),
            "created_by": user_uid,
            "program": program_data, # This is your 'weeks' nested JSON
            "stats": {
                "weeks": st.session_state.get('program_builder_desktop_num_weeks'),
                "days_per_week": st.session_state.get('program_builder_desktop_num_days')
            }
        }

        # 4. Perform the write
        doc_ref.set(payload)
        return True

    except Exception as e:
        st.error(f"Firestore Save Failed: {str(e)}")
        return False