"""
api.py

Provides a accessible protected backend API. JSON I/O only, CSRF protected.
"""
import copy
import json
import os
from copy import deepcopy

import flask_wtf
from flask import current_app, jsonify, request

from server.helpers import default, get_neighbors

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, 'data', 'data.json'), 'r', encoding='utf-8') as file:
    data = json.load(file)

with open(os.path.join(BASE_DIR, 'data', 'characters.json'), 'r', encoding='utf-8') as file:
    character_data = json.load(file)

# Cached preload character data
character_list = dict()

stats = {
    'totals': {
        'quote': 0,
        'scene': 0,
        'episode': 0,
        'season': 0
    }
}

stats['totals']['season'] += len(default(data, []))
for season in data:
    stats['totals']['episode'] += len(default(season.get('episodes'), []))
    for episode in season['episodes']:
        stats['totals']['scene'] += len(default(episode.get('scenes'), []))
        for scene in default(episode.get('scenes'), []):
            stats['totals']['quote'] += len(default(scene.get('quotes'), []))


@current_app.route('/api/csrf/')
def api_csrf():
    """
    Page used for refreshing expired CSRF tokens via AJAX.

    Probably secure: https://medium.com/@iaincollins/csrf-tokens-via-ajax-a885c7305d4a
    """
    return jsonify(flask_wtf.csrf.generate_csrf())


@current_app.route('/api/episode/<int:season>/<int:episode>/')
def api_episode(season: int, episode: int):
    return jsonify(data[season - 1]['episodes'][episode - 1])


@current_app.route('/api/stats/')
def api_stats():
    return jsonify(stats)


@current_app.route('/api/episodes/')
def api_episodes():
    """
    Returns a list of episodes with basic information (no quotes).
    Used for the left side season bar.
    """
    seasons = []
    copy = deepcopy(data)
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


@current_app.route('/api/quote_surround')
def api_quote_neighbors():
    season, episode = int(request.args.get('season')), int(request.args.get('episode'))
    scene, quote = int(request.args.get('scene')), int(request.args.get('quote'))

    quotes = data[season - 1]['episodes'][episode - 1]['scenes'][scene - 1]['quotes']
    top, below = get_neighbors(quotes, quote - 1, int(request.args.get('distance', 2)))
    return jsonify({'above': top, 'below': below})


@current_app.route('/api/characters/')
def api_character_list():
    return jsonify(list(character_data.keys()))


@current_app.route('/api/character/<character>/')
def api_character_all(character: str):
    _data = copy.deepcopy(character_data[character])
    _data['quotes'] = _data['quotes'][:10]
    return jsonify(_data)


@current_app.route('/api/character/<character>/quotes/')
def api_character_quotes(character: str):
    quotes = character_data[character]['quotes']

    # Compute pagination if argument is available. Static 10 results per page, one-indexed.
    if 'page' in request.args.keys():
        index: int = (int(request.args['page']) - 1) * 10
        return jsonify(quotes[index: index + 10])
    else:
        return jsonify(quotes)
