"""
api.py

Provides a accessible protected backend API. JSON I/O only, CSRF protected.
"""
import flask_wtf
from flask import current_app, jsonify


@current_app.route('/api/csrf/')
def csrf():
    """
    Page used for refreshing expired CSRF tokens via AJAX.

    Probably secure: https://medium.com/@iaincollins/csrf-tokens-via-ajax-a885c7305d4a
    """
    return jsonify(flask_wtf.csrf.generate_csrf())
