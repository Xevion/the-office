"""
create_app.py

The create_app function used to create and initialize the app with all of it's extensions and settings.
"""
import json
import os

from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from sassutils.wsgi import SassMiddleware
from werkzeug.exceptions import HTTPException

from the_office.config import configs

csrf = CSRFProtect()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def create_app(env=None):
    """
    The create_app function used to create and initialize the app with all of it's extensions and settings.
    """
    app = Flask(__name__)

    # Add Sass middleware (black magic)
    app.wsgi_app = SassMiddleware(app.wsgi_app, {
        'the_office': ('static/sass', 'static/css', '/static/css', False)
    })

    # Load configuration values
    if not env:
        env = app.config['ENV']
    app.config.from_object(configs[env])

    # Fixes poor whitespace rendering in templates
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True

    # Initialize Flask extensions
    csrf.init_app(app)

    # flask_static_digest.init_app(app)
    # CLI commands setup
    @app.shell_context_processor
    def shell_context():
        """Provides specific Flask components to the shell."""
        return {'app': app}

    # Custom error handler page (all errors)
    @app.errorhandler(HTTPException)
    def handle_exception(e):
        """Error handler, sends users to a custom error page template."""
        return render_template('error.html', exception=e), e.code

    @app.context_processor
    def inject_debug():
        """
        Allows for testing for debug mode in jinja2 templates.
        """
        return dict(debug=app.debug)

    @app.context_processor
    def inject_data():
        with open(os.path.join(BASE_DIR, 'data', 'data.json'), 'r', encoding='utf-8') as file:
            return dict(data=json.load(file))

    # noinspection PyUnresolvedReferences
    with app.app_context():
        # noinspection PyUnresolvedReferences
        from the_office import routes

    return app
