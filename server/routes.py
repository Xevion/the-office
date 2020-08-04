from flask import current_app, render_template, abort

from server.helpers import check_validity


@current_app.route('/')
def index():
    """Index page."""
    return render_template('index.html')


@current_app.route('/<int:season>')
def view_season(season):
    if not check_validity(season, 1):
        abort(404)
    return render_template('season.html', season=season)


@current_app.route('/<int:season>/<int:episode>')
def view_episode(season, episode):
    if not check_validity(season, episode):
        abort(404)
    return render_template('episode.html', season=season, episode=episode)
