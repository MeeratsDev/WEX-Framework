from imports import *


# Middleware to verify Firebase token
def verify_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            print("Auth Error: No Authorization header found")
            return jsonify({"error": "Missing token"}), 401

        try:
            # Safely extract the token
            parts = auth_header.split(" ")
            token = parts[1] if len(parts) > 1 else parts[0]

            # This is the line that is likely failing
            decoded_token = auth.verify_id_token(token)
            request.user_id = decoded_token["uid"]
        except Exception as e:
            # This will print the EXACT reason (e.g., "Token expired", "Invalid signature")
            print(f"Firebase Auth Error: {str(e)}")
            return jsonify({"error": "Invalid token", "details": str(e)}), 401

        return f(*args, **kwargs)

    return decorated_function
