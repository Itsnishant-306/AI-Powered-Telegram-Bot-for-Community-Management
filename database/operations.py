# database/operations.py
import os
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Firebase
cred = credentials.Certificate(os.getenv('FIREBASE_CREDENTIALS'))
firebase_admin.initialize_app(cred)
db = firestore.client()

def create_user_if_not_exists(user_id, username, first_name):
    """Create a user in the database if they don't exist."""
    user_ref = db.collection('users').document(str(user_id))
    user = user_ref.get()
    
    if not user.exists:
        user_ref.set({
            'username': username,
            'first_name': first_name,
            'joined_at': firestore.SERVER_TIMESTAMP,
            'is_active': True
        })
        return True
    return False

def init_db():
    """Check if the Firebase connection is working."""
    try:
        # Try accessing the database to ensure connection
        db.collection('test').document('connection_test').set({'status': 'ok'})
        print("✅ Firebase database initialized successfully!")
    except Exception as e:
        print(f"❌ Error initializing Firebase: {e}")


def save_message(user_id, message_text, is_bot=False):
    """Save a message to the database."""
    message_ref = db.collection('messages').document()
    message_ref.set({
        'user_id': str(user_id),
        'message': message_text,
        'is_bot': is_bot,
        'timestamp': firestore.SERVER_TIMESTAMP
    })

    # Add to database/operations.py

def increment_user_points(user_id, points=1):
    """Increment user's engagement points."""
    user_ref = db.collection('users').document(str(user_id))
    user = user_ref.get()
    
    if user.exists:
        current_points = user.to_dict().get('points', 0)
        user_ref.update({
            'points': current_points + points
        })
        return current_points + points
    return 0

def get_active_users():
    """Retrieve all active users from the database."""
    users_ref = db.collection('users').where('is_active', '==', True)
    users = users_ref.stream()
    
    active_users = []
    for user in users:
        user_data = user.to_dict()
        active_users.append({
            'user_id': user.id,
            'username': user_data.get('username', 'Anonymous'),
            'first_name': user_data.get('first_name', '')
        })
    
    return active_users

def get_leaderboard(limit=10):
    """Get the top users by points."""
    users_ref = db.collection('users').order_by('points', direction=firestore.Query.DESCENDING).limit(limit)
    users = users_ref.stream()
    
    leaderboard = []
    for user in users:
        user_data = user.to_dict()
        leaderboard.append({
            'user_id': user.id,
            'username': user_data.get('username', 'Anonymous'),
            'points': user_data.get('points', 0)
        })
    
    return leaderboard

def get_all_users():
    """Retrieve all users from Firebase Firestore."""
    users_ref = db.collection('users').stream()  # Get all user documents
    users_list = []
    
    for user in users_ref:
        user_data = user.to_dict()
        user_data["user_id"] = user.id  # Add user ID to data
        users_list.append(user_data)

    return users_list
