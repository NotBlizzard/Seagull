from dotenv import load_dotenv
from flask import Flask
from auth import login_manager
from flask_bcrypt import Bcrypt
from authlib.integrations.flask_client import OAuth
app = Flask(__name__)
oauth = OAuth(app)
login_manager.init_app(app)
bcrypt = Bcrypt(app)

load_dotenv()
