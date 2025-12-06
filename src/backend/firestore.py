from google.cloud import firestore
import streamlit as st


# --- CONFIGURATION (MUST MATCH YOUR SETUP) ---
CUSTOM_DB_NAME = 'training-log' 
COLLECTION_NAME = 'activePrograms'
DOCUMENT_ID = 'workout_v1_0'


@st.cache_resource
def get_firestore_client():
    # Pass the database name explicitly for custom-named databases
    return firestore.Client.from_service_account_info(
        st.secrets["firestore"],
        database=CUSTOM_DB_NAME
    )

db = get_firestore_client()

@st.cache_data(ttl=3600)
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

CUSTOM_DB_NAME = 'training-log' 
COLLECTION_NAME = 'activePrograms'
DOCUMENT_ID = 'workout_v1_0'
def upload_program_json(program: dict):
    doc_ref = db.collection(COLLECTION_NAME).document(DOCUMENT_ID)
    doc_ref.set(program)