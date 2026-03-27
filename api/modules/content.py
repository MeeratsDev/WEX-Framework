from imports import *


# Get show episode details
@app.route("/api/show/<show_name>/<season>/<episode>", methods=["GET"])
def get_show(show_name, season, episode):
    try:
        doc = (
            db.collection("shows")
            .document(show_name)
            .collection(season)
            .document(episode)
            .get()
        )
        if doc.exists:
            episode_data = doc.to_dict()
            return jsonify(episode_data), 200
        return jsonify({"error": "Episode not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/show/<show_name>/<season>/episodes", methods=["GET"])
def get_episodes(show_name, season):
    try:
        episodes = db.collection("shows").document(show_name).collection(season).count()
        return jsonify({"episodes": episodes}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
