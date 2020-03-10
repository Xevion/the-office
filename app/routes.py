from flask import send_from_directory, redirect, url_for, render_template, request
from app.models import Season, Episode, Quote
from app import app


@app.route("/")
def index():
    return render_template("home.html", seasons=Season.query.all(), nquotes=len(Quote.query.all()), nepisodes=len(Episode.query.all()))


@app.route("/view/<season>/")
def viewSeason(season):
    return render_template(
        "season.html", season=Season.query.filter_by(id=season).first_or_404(), seasons=Season.query.all()
    )

@app.route("/view/<season>/<episode>/")
def viewEpisode(season, episode):
    e = Episode.query.filter_by(season_id=season, number=episode).first_or_404()
    if not e.built:
        print("Rebuilding")
        e.build()
    return render_template("episode.html", episode=e, seasons=Season.query.all())


@app.route("/redownload/<season>")
def rebuildSeason(season):
    season = Season.query.filter_by(id=season).first_or_404()
    season.rebuild()
    return redirect(url_for("viewSeason", season=season.id))

@app.route("/redownload/<season>")
def rebuildSeason(season):
    seasonObj = Season.query.filter_by(id=season).first_or_404()
    seasonObj.redownload_all()
    return redirect(url_for("viewSeason", season=season))

@app.route("/rebuild/<season>/<episode>/")
def rebuildEpisode(season, episode):
    e = Episode.query.filter_by(season_id=season, number=episode).first_or_404()
    e.rebuild()
    return redirect(url_for("viewEpisode", season=season, episode=episode))

@app.route("/redownload/<season>/<episode>/")
def redownloadEpisode(season, episode):
    e = Episode.query.filter_by(season_id=season, number=episode).first_or_404()
    e.download(force=True)
    return redirect(url_for("viewEpisode", season=season, episode=episode))

