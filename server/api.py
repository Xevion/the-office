"""
api.py

Provides a accessible protected backend API. JSON I/O only, CSRF protected.
"""
import json
import os

import flask_wtf
from flask import current_app, jsonify

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, 'data', 'data.json'), 'r', encoding='utf-8') as file:
    data = json.load(file)


@current_app.route('/api/csrf/')
def api_csrf():
    """
    Page used for refreshing expired CSRF tokens via AJAX.

    Probably secure: https://medium.com/@iaincollins/csrf-tokens-via-ajax-a885c7305d4a
    """
    return jsonify(flask_wtf.csrf.generate_csrf())


@current_app.route('/api/episodes/')
def api_episodes():
    """
    Returns a list of episodes with basic information (no quotes).
    Used for the left side season bar.
    """
    seasons = []
    copy = list(data)
    for season in copy:
        for episode in season.get('episodes'):
            if 'scenes' in episode.keys():
                del episode['scenes']
        seasons.append(season)
    return jsonify(seasons)


@current_app.route('/api/all/')
def api_data():
    """
    Season data route
    """
    return jsonify(data)
