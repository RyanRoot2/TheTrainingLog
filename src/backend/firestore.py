from google.cloud import firestore
import streamlit as st
from typing import Any

# Constants
# Names for the database, collections, and subcollections
DB_NAME = 'training-log' 
USERS_COLLECTION = 'users'
USER_PROGRAM_TEMPLATES_SUBCOLLECTION = 'user_program_templates' # Blank templates of any programs the user has created
USER_STARTED_PROGRAMS_SUBCOLLECTION = 'user_started_programs' # Programs the user has made "active" / started - copies of templates
GLOBAL_PROGRAM_TEMPLATES_COLLECTION = 'global_program_templates' # Pre-made templates provided by the app

# Types
ProgramData = dict[str, Any]


@st.cache_resource
def get_firestore_client() -> firestore.Client:
    """Initializes and returns a Firestore client. Stores the client as a cached resource"""
    # Pass the database name explicitly for custom-named databases
    return firestore.Client.from_service_account_info(
        st.secrets["firestore"],
        database=DB_NAME
    )
# Initialize Firestore client immediately - try to remove this and see what happens, use the "call everywhere" approach instead
db = get_firestore_client()


def get_active_program_id() -> str | None:
    """Returns the active program ID for the current user."""
    user_uid = st.session_state.get("user_uid")
    assert user_uid is not None, "Attempted to get active program ID without a valid user_uid in session state."
    db = get_firestore_client()

    user_doc = db.collection(USERS_COLLECTION).document(user_uid).get()
    return user_doc.get("active_program_id") # Returns None if no active program is set


@st.cache_data(ttl=3600*4)  # Cache for 4 hours
def load_active_program_json() -> ProgramData | None:
    """Loads the active program JSON for the current user from Firestore."""
    user_uid = st.session_state.get("user_uid")
    assert user_uid is not None, "Attempted to load active program without a valid user_uid in session state."
    db = get_firestore_client()
    active_program_id = get_active_program_id()
    active_program = db.collection(USERS_COLLECTION).document(user_uid)\
            .collection(USER_STARTED_PROGRAMS_SUBCOLLECTION)\
            .document(active_program_id).get()

    if not active_program.exists:
        return None
    
    return active_program.to_dict()


def copy_to_started_and_return_id(template_id: str) -> str:
    """Copies a program template to the user's started programs and returns the new program ID."""
    user_uid = st.session_state.get("user_uid")
    assert user_uid is not None, "Attempted to copy template without a valid user_uid in session state."
    db = get_firestore_client()

    # Get the template data - returns a snapshot object, not just the raw data
    template_doc = db.collection(USERS_COLLECTION).document(user_uid)\
        .collection(USER_PROGRAM_TEMPLATES_SUBCOLLECTION)\
        .document(template_id).get()
    assert template_doc.exists, f"Template with ID {template_id} does not exist."

    # Add the template data to the user's started programs
    # The add() method returns a tuple of (DocumentReference, new_document_id)
    _, doc_ref = db.collection(USERS_COLLECTION).document(user_uid)\
        .collection(USER_STARTED_PROGRAMS_SUBCOLLECTION)\
        .add(template_doc.to_dict()) # to_dict gets the raw data from the snapshot

    # Return the new program ID
    return doc_ref.id


def set_active_program_id(program_id: str) -> None:
    """Sets the active program ID for the current user."""
    user_uid = st.session_state.get("user_uid")
    assert user_uid is not None, "Attempted to set active program ID without a valid user_uid in session state."
    db = get_firestore_client()

    user_doc_ref = db.collection(USERS_COLLECTION).document(user_uid)
    user_doc_ref.update({"active_program_id": program_id})


def get_all_user_templates():
    db = get_firestore_client()
    user_uid = st.session_state.get("user_uid")
    assert user_uid is not None, "Attempted to get user templates without a valid user_uid in session state."

    templates_ref = db.collection(USERS_COLLECTION).document(user_uid).collection(USER_PROGRAM_TEMPLATES_SUBCOLLECTION)
    docs = templates_ref.order_by("template_name", direction="DESCENDING").stream()

    return [{**doc.to_dict(), "id": doc.id} for doc in docs] # Return list of dicts with template data and document ID as "id", [] if empty


def update_program_in_firestore(program_id: str, program_data: ProgramData) -> None:
    """Updates the program data for a given program ID in Firestore."""
    user_uid = st.session_state.get("user_uid")
    assert user_uid is not None, "Attempted to update program without a valid user_uid in session state."
    db = get_firestore_client()

    program_doc_ref = db.collection(USERS_COLLECTION).document(user_uid)\
        .collection(USER_STARTED_PROGRAMS_SUBCOLLECTION).document(program_id)
    
    program_doc_ref.set(program_data, merge=True)

    load_active_program_json.clear()  # Clear the cache for the active program JSON