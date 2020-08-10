"""
create_app.py

The create_app function used to create and initialize the app with all of it's extensions and settings.
"""

from flask import Flask, render_template
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect

from server.config import configs

csrf = CSRFProtect()
cors = CORS(resources={r'/api/*': {'origins': '*'}})


def create_app(env=None):
    """
    The create_app function used to create and initialize the app with all of it's extensions and settings.
    """
    app = Flask(__name__,
                static_folder="./../dist/static",
                template_folder="./../dist"
                )

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

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def catch_all(path):
        return render_template("index.html")

    return app
