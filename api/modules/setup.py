from imports import *

# Set up paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app = Flask(__name__, static_folder=BASE_DIR, static_url_path="")

load_dotenv()
