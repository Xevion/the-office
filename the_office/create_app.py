"""
create_app.py

The create_app function used to create and initialize the app with all of it's extensions and settings.
"""

from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from sassutils.wsgi import SassMiddleware
from werkzeug.exceptions import HTTPException
from flask_static_digest import FlaskStaticDigest

from the_office.config import configs

# flask_static_digest = FlaskStaticDigest()
db = SQLAlchemy()
csrf = CSRFProtect()
migrate = Migrate()


def create_app(env=None):
    """
    The create_app function used to create and initialize the app with all of it's extensions and settings.
    """
    app = Flask(__name__)

    # Add Sass middleware (black magic)
    app.wsgi_app = SassMiddleware(app.wsgi_app, {
        'unimatch': ('static/sass', 'static/css', '/static/css', False)
    })

    # Load configuration values
    if not env:
        env = app.config['ENV']
    app.config.from_object(configs[env])

    # Fixes poor whitespace rendering in templates
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True

    # Initialize Flask extensions
    db.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)

    # flask_static_digest.init_app(app)
    # CLI commands setup
    @app.shell_context_processor
    def shell_context():
        """Provides specific Flask components to the shell."""
        return {'app': app, 'db': db}

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

    # noinspection PyUnresolvedReferences
    from unimatch import models
    with app.app_context():
        db.create_all()
        # noinspection PyUnresolvedReferences
        from unimatch import routes

    # Register custom commands
    from unimatch import commands
    app.cli.add_command(commands.load_colleges)

    return app
