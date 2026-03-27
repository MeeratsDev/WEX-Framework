import modules.accounts
import modules.content
import modules.setup
import modules.verification
from modules.imports import *

app = modules.setup.app
BASE_DIR = modules.setup.BASE_DIR


# Serve static files
@app.route("/")
def index():
    return send_from_directory(BASE_DIR, "index.html")


@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(BASE_DIR, filename)


if __name__ == "__main__":
    app.run(debug=True)
