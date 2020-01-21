from flask import send_from_directory, redirect, url_for, render_template, request
from app.models import Season, Episode
from app import app

@app.route('/')
def index():
    return 'WIP'

@app.route('/view')
def view():
    season = request.args.get('season', default=-1, type=int)
    episode = request.args.get('episode', default=-1, type=int)

    if season != -1:
        if episode != -1:
            return render_template('episode.html', episode=Episode.query.filter_by(season_id=season, number=episode).first_or_404())
        else:
            return render_template('season.html', season=Season.query.filter_by(id=season).first_or_404())
    return redirect(url_for('index'))