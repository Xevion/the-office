# Main Flask and Flask configs
from flask import Flask
from config import Config
# Flask Extensions
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# App & App config setup
app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
# App extension setup
login = LoginManager(app)
login.login_view = 'login'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
limiter = Limiter(app, key_func=get_remote_address, default_limits=["10 per second"])