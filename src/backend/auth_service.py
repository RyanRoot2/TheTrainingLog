from firebase_admin import auth, exceptions
from src.backend.firestore import db
from google.cloud import firestore

def get_or_create_user(email: str):
    try:
        user_record = auth.get_user_by_email(email)
        return user_record
    except exceptions.NotFoundError:
        print(f"User {email} not found. Creating new user...")
        user_record = auth.create_user(email=email)
        return user_record
    
def ensure_firestore_user_document(uid: str, email: str):
    """
    Checks if a document exists for this UID in Firestore.
    If not, initializes a new empty user profile.
    """
    user_ref = db.collection("users").document(uid)
    
    # Check if document exists
    doc = user_ref.get()
    
    if not doc.exists:
        # Initialize default data structure for a new user
        default_data = {
            "email": email,
            "created_at": firestore.SERVER_TIMESTAMP,
            "active_program_id": None, # User hasn't selected a program yet
            "settings": {}
        }
        user_ref.set(default_data)
        print(f"Created new Firestore profile for {uid}")