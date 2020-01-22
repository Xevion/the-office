from flask import send_from_directory, redirect, url_for, render_template, request
from app.models import Season, Episode
from app import app

@app.route('/')
def index():
    return render_template('view.html', seasons=Season.query.all())

@app.route('/season/<season>/')
def season(season):
    return render_template('season.html', season=Season.query.filter_by(id=season).first_or_404())
    
@app.route('/season/<season>/<episode>')
def episode(season, episode):
    return render_template('episode.html', episode=Episode.query.filter_by(season_id=season, number=episode).first_or_404())