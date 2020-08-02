from flask import current_app, render_template


@current_app.route('/')
def index():
    """Index page."""
    return render_template('index.html')


@current_app.route('/<int:season>')
def view_season(season):
    return render_template('season.html', season=season)


@current_app.route('/<int:season>/<int:episode>')
def view_episode(season, episode):
    return render_template('episode.html', season=season, episode=episode)
