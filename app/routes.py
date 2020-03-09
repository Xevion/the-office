from flask import send_from_directory, redirect, url_for, render_template, request
from app.models import Season, Episode
from app import app


@app.route("/")
def index():
    return render_template("view.html", seasons=Season.query.all())


@app.route("/season/<season>/")
def viewSeason(season):
    return render_template(
        "season.html", season=Season.query.filter_by(id=season).first_or_404()
    )


@app.route("/season/<season>/<episode>/")
def viewEpisode(season, episode):
    e = Episode.query.filter_by(season_id=season, number=episode).first_or_404()
    if not e.built:
        print("Rebuilding")
        e.build()
    return render_template("episode.html", episode=e)


@app.route("/season/<season>/<episode>/rebuild")
def rebuildEpisode(season, episode):
    e = Episode.query.filter_by(season_id=season, number=episode).first_or_404()
    e.rebuild()
    return redirect(url_for("viewEpisode", season=season, episode=episode))
