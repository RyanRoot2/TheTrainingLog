import streamlit as st
from src.backend.auth_service import get_or_create_user, ensure_firestore_user_document

SESSION_KEY_UID = "user_uid"
SESSION_KEY_LOGGED_IN = "is_logged_in"

def authenticate_user_and_update_session():
    # 1. Standard Streamlit OIDC check
    if st.session_state.get(SESSION_KEY_LOGGED_IN):
        return True

    try:
        # Safe check for OIDC object
        if not hasattr(st.user, "is_logged_in") or not st.user.is_logged_in:
            return False
    except Exception:
        # Fallback for local/config errors
        st.stop()

    # --- User is Authenticated via Google ---
    oidc_email = st.user.email

    # 2. Call the Backend (Abstraction)
    # Get the Identity (UID)
    user_record = get_or_create_user(oidc_email)
    
    # 3. Ensure the Database Record Exists
    # This creates the "users/{uid}" document if it's their first time
    ensure_firestore_user_document(user_record.uid, oidc_email)

    # 4. Save to Session
    st.session_state[SESSION_KEY_UID] = user_record.uid
    st.session_state[SESSION_KEY_LOGGED_IN] = True
    st.session_state["user_email"] = oidc_email
    
    return True


def enforce_login():
    """
    The central function called at the top of every Streamlit page.
    If the user is not authenticated, it stops the script and forces the login UI.
    """
    
    # Path A: Already logged in, nothing to do.
    if st.session_state.get(SESSION_KEY_LOGGED_IN):
        return True
    
    # Path B: Not in session state, try to complete the OIDC flow
    if authenticate_user_and_update_session():
        # Success! State is updated. Rerun the script to complete the redirect.
        st.rerun()
    else:
        # Path C: Authentication failed/not yet started. Display login UI and stop.
        st.title("Trainer App 🏋️")
        st.info("Please log in to access your workout programs.")
        st.button("Log in with Google", on_click=st.login)
        st.stop()