import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

@st.cache_resource
def initialise_firebase_admin():
    """Initialise the Firebase Admin SDK using st.secrets"""

    # Check if a named app already exists
    if not firebase_admin._apps or 'admin_app' not in firebase_admin._apps:
        try:
            cred_dict = dict(st.secrets['firebase']) # Retrieve creds
            cred = credentials.Certificate(cred_dict) # Create Creds object
            firebase_admin.initialize_app(credential=cred) # Initialise app

            firebase_admin.get_app() # Get the admin app
       
        except KeyError as e:
            st.error(f"FATAL ERROR: Firebase secret key {e} not found.")
            st.stop()
        except Exception as e:
            st.error(f"FATAL ERROR: Failed to initialise Firebase: {e}.")
            st.stop()

    return firestore.client()

AUTH_CLIENT = initialise_firebase_admin()
