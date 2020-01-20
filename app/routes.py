from flask import send_from_directory, redirect, url_for, render_template, request
from app.models import Season, Episode
from app import app

@app.route('/')
def index():
    return 'WIP'

@app.route('/view')
def view():
    seasonID = request.args.get('season')
    episodeNUM = request.args.get('episode')

    season = Season.query.get(int(seasonID))
    episode = Episode.query.filter_by(season_id=season.id, number=int(episodeNUM))

    if season:
        if episode:
            return render_template('episode.html')
        else:
            return render_template('season.html', season=Season.query.get())
    return redirect(url_for('index'))