from imports import *

# Initialize Firebase
try:
    cred_path = os.getenv("FIREBASE_SERVICE_ACCOUNT")
    print("FIREBASE_SERVICE_ACCOUNT:", cred_path)
    if cred_path:
        cred_data = json.loads(cred_path)
        print("Loaded Firebase credentials from environment variable.", cred_data)
    else:
        raise ValueError("FIREBASE_SERVICE_ACCOUNT environment variable not set")

    cred = credentials.Certificate(cred_data)
    firebase_admin.initialize_app(cred)
    print("Firebase initialized with provided credentials.")
except ValueError:
    firebase_admin.initialize_app()

db = firestore.client()


@app.route("/api/config/firebase/client")
def get_config():
    return jsonify(
        {
            "apiKey": os.getenv("FIREBASE_API_KEY"),
            "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
            "projectId": os.getenv("FIREBASE_PROJECT_ID"),
            "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
            "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
            "appId": os.getenv("FIREBASE_APP_ID"),
            "measurementId": os.getenv("FIREBASE_MEASUREMENT_ID"),
        }
    )
