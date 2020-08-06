"""
create_app.py

The create_app function used to create and initialize the app with all of it's extensions and settings.
"""

from flask import Flask
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect

from server.config import configs

csrf = CSRFProtect()
cors = CORS(resources={r'/*': {'origins': '*'}})


def create_app(env=None):
    """
    The create_app function used to create and initialize the app with all of it's extensions and settings.
    """
    app = Flask(__name__)

    # Load configuration values
    if not env:
        env = app.config['ENV']
    app.config.from_object(configs[env])

    # Initialize Flask extensions
    csrf.init_app(app)
    cors.init_app(app)

    # CLI commands setup
    @app.shell_context_processor
    def shell_context():
        """Provides specific Flask components to the shell."""
        return {'app': app}

    with app.app_context():
        # noinspection PyUnresolvedReferences
        from server import api

    return app
