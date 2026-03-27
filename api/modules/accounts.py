from imports import *


# User registration
@app.route("/api/auth/register", methods=["POST"])
def register():
    try:
        email = request.json.get("email")
        password = request.json.get("password")
        name = request.json.get("name", "")

        if not email or not password or len(password) < 8:
            return jsonify({"error": "Invalid email or password (min 8 chars)"}), 400

        user = auth.create_user(email=email, password=password, display_name=name)
        db.collection("users").document(user.uid).set(
            {
                "name": name,
                "email": email,
                "phone": "",
                "location": "",
                "subscriptions": "Free",
                "status": "Pending",
                "renewal": "",
                "profilepic": "images/profiles/profile-blue.png",
            }
        )

        return jsonify({"uid": user.uid, "message": "User created"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# User login
@app.route("/api/auth/login", methods=["POST"])
def login():
    print("API Hit: Login request received")
    try:
        id_token = request.json.get("idToken")
        if not id_token:
            return jsonify({"error": "Missing ID token"}), 400

        decoded_token = auth.verify_id_token(id_token)
        print("Decoding Token:", id_token)
        print("Decoded Token:", decoded_token)
        user_id = decoded_token["uid"]
        print("Token verified for UID:", decoded_token["uid"])

        # Fetch user profile
        try:
            print("attempting to fetch user document for UID:", user_id)
            user_doc = db.collection("users").document(user_id).get()
            print(
                "Fetched User Document:",
                user_doc.to_dict() if user_doc.exists else "No document found",
            )
        except Exception as error:
            print("Error fetching user document:", str(error))
            return jsonify({"error": "Failed to fetch user data"}), 500
        user_data = user_doc.to_dict() if user_doc.exists else {}
        print("User Data Acquired:", user_data)

        print(
            "returning response",
            {"uid": user_id, "message": "Login successful", "user": user_data},
        )
        return jsonify(
            {"uid": user_id, "message": "Login successful", "user": user_data}
        ), 200
    except Exception as e:
        return jsonify({"error": "Invalid credentials"}), 401


# Get user account
@app.route("/api/users/<user_id>/account", methods=["GET"])
@verify_token
def get_account(user_id):
    if not user_id:
        user_id = request.headers.get("user_id")

    try:
        print("Fetching account for UID:", user_id)
        doc = db.collection("users").document(user_id).get()
        if doc.exists:
            print("account data acquired:", doc.to_dict())
            return jsonify(doc.to_dict()), 200
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Update user account
@app.route("/api/users/<user_id>/account", methods=["PUT"])
@verify_token
def update_account(user_id):
    try:
        db.collection("users").document(user_id).update(request.json)
        return jsonify({"message": "Account updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/users/<user_id>/profiles", methods=["GET"])
@verify_token
def get_profiles(user_id):
    try:
        profiles = (
            db.collection("users").document(user_id).collection("profiles").stream()
        )
        profile_list = {doc.id: doc.to_dict() for doc in profiles}
        return jsonify(profile_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/users/<user_id>/profiles/delete/<profile_name>", methods=["DELETE"])
@verify_token
def delete_profile(user_id, profile_name):
    profile_name = unquote(profile_name)
    try:
        db.collection("users").document(user_id).collection("profiles").document(
            profile_name
        ).delete()
        return jsonify({"message": "Profile deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Update profile picture
@app.route("/api/users/<user_id>/profiles/<profile_name>/profilepic", methods=["PUT"])
@verify_token
def update_profile_pic(user_id, profile_name):
    profile_name = unquote(profile_name)
    try:
        new_pic_url = request.json.get("profilePic")
        db.collection("users").document(user_id).collection("profiles").document(
            profile_name
        ).update({"profilePic": new_pic_url})
        return jsonify({"message": "Profile picture updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Continue watching
@app.route(
    "/api/users/<user_id>/profiles/<profile_name>/<dynamic_row>", methods=["GET"]
)
@verify_token
def continue_watching(user_id, dynamic_row, profile_name):
    profile_name = unquote(profile_name)
    try:
        if request.method == "GET":
            docs = (
                db.collection("users")
                .document(user_id)
                .collection("profiles")
                .document(profile_name)
                .collection(dynamic_row)
                .stream()
            )
            items = [doc.to_dict() for doc in docs]
            return jsonify(items), 200

        return jsonify({"message": "Added to continue watching"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route(
    "/api/users/<user_id>/profiles/<profile_name>/<dynamic_row>/<item_id>",
    methods=["DELETE"],
)
@verify_token
def remove_continue_watching(user_id, profile_name, dynamic_row, item_id):
    profile_name = unquote(profile_name)
    try:
        db.collection("users").document(user_id).collection("profiles").document(
            profile_name
        ).collection(dynamic_row).document(item_id).delete()
        return jsonify({"message": "Removed from " + dynamic_row}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route(
    "/api/users/<user_id>/profiles/<profile_name>/<dynamic_row>/<item_id>",
    methods=["POST"],
)
@verify_token
def add_to_dynamic(user_id, profile_name, dynamic_row, item_id):
    profile_name = unquote(profile_name)
    try:
        db.collection("users").document(user_id).collection("profiles").document(
            profile_name
        ).collection(dynamic_row).document(item_id).set({"id": item_id})
        return jsonify({"message": "Added to " + dynamic_row}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/<user_id>/profiles/<profile_name>", methods=["GET", "PATCH"])
@verify_token
def get_profile(user_id, profile_name):
    profile_name = unquote(profile_name)
    print("Request type: " + request.method)
    if request.method == "GET":
        try:
            doc = (
                db.collection("users")
                .document(user_id)
                .collection("profiles")
                .document(profile_name)
                .get()
            )
            if doc.exists:
                return jsonify(doc.to_dict()), 200
            return jsonify({"error": "Profile not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    elif request.method == "PATCH":
        print("Attempting to use PATCH logic")
        try:
            data = request.json
            if not data:
                return jsonify({"error": "No data provided"}), 400

            print("Data acquired " + str(data))
            db.collection("users").document(user_id).collection("profiles").document(
                profile_name
            ).update(data)
            return jsonify({"success": True, "message": "Profile updated"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500


@app.route("/api/users/<user_id>/profiles/create", methods=["POST"])
@verify_token
def create_profile(user_id):
    try:
        profile_name = request.json.get("profileName")
        age_group = request.json.get("ageGroup")
        profile_pic = request.json.get("profilePic")
        profile_data = {
            "name": profile_name,
            "profilePic": profile_pic,
            "ageGroup": age_group,
        }
        db.collection("users").document(user_id).collection("profiles").document(
            profile_name
        ).set(profile_data)
        return jsonify({"message": "Profile created"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
